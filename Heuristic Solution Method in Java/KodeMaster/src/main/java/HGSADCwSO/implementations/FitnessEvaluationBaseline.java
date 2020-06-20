package main.java.HGSADCwSO.implementations;

import main.java.HGSADCwSO.files.Individual;
import main.java.HGSADCwSO.files.ProblemData;
import main.java.HGSADCwSO.files.Utilities;
import main.java.HGSADCwSO.implementations.DAG.Node;
import main.java.HGSADCwSO.protocols.FitnessEvaluationProtocol;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class FitnessEvaluationBaseline implements FitnessEvaluationProtocol {

    private ProblemData problemData;

    private double nCloseProp;
    protected double nEliteProp;
    private double numberOfOrders;

    protected double durationViolationPenalty;
    protected double capacityViolationPenalty;
    protected double deadlineViolationPenalty;

    private HashMap<Individual, HashMap<Individual, Double>> hammingDistances;

    public FitnessEvaluationBaseline(ProblemData problemData){
        this.problemData = problemData;

        this.hammingDistances = new HashMap<Individual, HashMap<Individual,Double>>();
        this.nCloseProp = problemData.getHeuristicParameterDouble("Proportion of individuals considered for distance evaluation");
        this.nEliteProp = problemData.getHeuristicParameterDouble("Proportion of elite individuals");
        this.numberOfOrders = problemData.getNumberOfOrders();

        this.capacityViolationPenalty = problemData.getHeuristicParameterDouble("Capacity constraint violation penalty");
        this.durationViolationPenalty = problemData.getHeuristicParameterDouble("Duration constraint violation penalty");
        this.deadlineViolationPenalty = problemData.getHeuristicParameterDouble("Deadline constraint violation penalty");
    }

    public void evaluate(Individual individual) {

    }

    public void updateBiasedFitness(ArrayList<Individual> population) {
        updateDiversityContribution(population);
        updatePenalizedCostRank(population);
        updateDiversityContributionRank(population);
        calculateBiasedFitness(population);
    }

    protected void updateDiversityContribution(ArrayList<Individual> population) {
        int nClose = (int) (population.size() * nCloseProp);
        for (Individual individual : population){
            ArrayList<Individual> nClosest = getnClosest(individual, nClose);
            double distance = 0;
            for (Individual close : nClosest){
                distance += hammingDistances.get(individual).get(close);
            }
            double diversityContribution = distance / nClose;
            individual.setDiversityContribution(diversityContribution);
        }
    }

    protected void updatePenalizedCostRank(ArrayList<Individual> population) {
        Collections.sort(population, Utilities.getPenalizedCostComparator());
        for (int i = 0; i < population.size(); i++){
            Individual individual = population.get(i);
            individual.setCostRank(i+1);
        }
    }

    protected void updateDiversityContributionRank(ArrayList<Individual> population) {
        Collections.sort(population, Utilities.getDiversityContributionComparator());
        for(int i = 0; i < population.size(); i++){
            Individual individual = population.get(i);
            individual.setDiversityRank(i+1);
        }
    }

    protected void calculateBiasedFitness(ArrayList<Individual> population) {
        int nIndividuals = population.size();
        double nElite = nIndividuals * nEliteProp;
        for (Individual individual : population){
            double biasedFitness = individual.getCostRank() + (1 - (nElite/nIndividuals)) * individual.getDiversityRank();
            individual.setBiasedFitness(biasedFitness);
        }
    }

    //The normalized Hamming distance counts the number of orders that are delivered with a different PSVs. Also the number of orders placed differently in a chromosome.
    public double getHammingDistance(Individual individual1, Individual individual2) {
        return hammingDistances.get(individual1).get(individual2);
    }

    public void setPenalizedCostIndividual(Individual individual, double durationViolationPenalty, double capacityViolationPenalty) {

    }

    public void addDiversityDistance(Individual individual) {
        HashMap<Individual, Double> individualHammingDistances = new HashMap<Individual, Double>();
        for (Individual existingIndividual : hammingDistances.keySet()){
            HashMap<Individual, Double> existingIndividualDistances = hammingDistances.get(existingIndividual);
            double normalizedHammingDistance = get_normalized_hamming_distance(individual, existingIndividual);
            existingIndividualDistances.put(individual, normalizedHammingDistance);
            individualHammingDistances.put(existingIndividual, normalizedHammingDistance);
            hammingDistances.put(existingIndividual, existingIndividualDistances);
        }
        hammingDistances.put(individual, individualHammingDistances);
    }

    public void removeDiversityDistance(Individual individual) {
        hammingDistances.remove(individual);
        for (Individual otherIndividual : hammingDistances.keySet()){
            hammingDistances.get(otherIndividual).remove(individual);
        }
    }

    public double get_normalized_hamming_distance(Individual individual_1, Individual individual_2) {
        HashMap<Integer, ArrayList<Integer>> chromosome_1 = Utilities.deepCopyVesselTour(individual_1.getVesselTourChromosome());
        HashMap<Integer, ArrayList<Integer>> chromosome_2 = Utilities.deepCopyVesselTour(individual_2.getVesselTourChromosome());
        int differance = 0;
        for (int vessel_number = 0; vessel_number < chromosome_1.size(); vessel_number++) {
            ArrayList<Integer> voyage_1_with_depot = chromosome_1.get(vessel_number);
            ArrayList<Integer> voyage_2_with_depot = chromosome_2.get(vessel_number);
            voyage_1_with_depot.add(0,0);
            voyage_2_with_depot.add(0,0);
            voyage_1_with_depot.add(0);
            voyage_2_with_depot.add(0);
        }
        for (int vessel_number_1 = 0; vessel_number_1 < chromosome_1.size(); vessel_number_1++) {
            for (int index_1 = 0; index_1 < chromosome_1.get(vessel_number_1).size() - 1; index_1 ++){

                int a = chromosome_1.get(vessel_number_1).get(index_1);
                int b = chromosome_1.get(vessel_number_1).get(index_1 + 1);
                boolean match = false;

                outerloop:
                for (int vessel_number_2 = 0; vessel_number_2 < chromosome_2.size(); vessel_number_2 ++) {
                    for (int index_2 = 0; index_2 < chromosome_2.get(vessel_number_2).size() - 1; index_2 ++ ) {

                        int c = chromosome_2.get(vessel_number_2).get(index_2);
                        int d = chromosome_2.get(vessel_number_2).get(index_2 + 1);

                        if (a == c && b == d) {
                            match = true;
                            break outerloop;
                        }
                    }
                }
                differance += match ? 0 : 1;
            }
        }
        int number_of_vessels = chromosome_1.size();
        return differance /(numberOfOrders + number_of_vessels);
    }


    public double getNormalizedHammingDistance(Individual individual1, Individual individual2) { //The normalized Hamming distance counts the number of orders that are delivered with different PSVs.
        HashMap<Integer, ArrayList<Integer>> chromosome1 = individual1.getVesselTourChromosome();
        HashMap<Integer, ArrayList<Integer>> chromosome2 = individual2.getVesselTourChromosome();

        int vesselDifference = 0;
        for (int vessel : chromosome1.keySet()){
            for (int order : chromosome1.get(vessel)){
                if (!chromosome2.get(vessel).contains(order)){
                    vesselDifference++;
                }
            }
        }

        int voyageDifference = 0;
        for (int vessel : chromosome1.keySet())
            for(int index = 0; index < chromosome1.get(vessel).size(); index++){
                if (chromosome1.get(vessel).size() > chromosome2.get(vessel).size()) {
                    if (index < chromosome2.get(vessel).size()){
                        if (chromosome2.get(vessel).get(index) != chromosome1.get(vessel).get(index)) {
                            voyageDifference++;
                        }
                    }
                    else if (index >= chromosome2.get(vessel).size()) {
                        voyageDifference += chromosome1.get(vessel).size() - chromosome2.get(vessel).size();
                        break;
                    }
                }
                else {
                    if (chromosome2.get(vessel).get(index) != chromosome1.get(vessel).get(index)) {
                        voyageDifference++;
                    }
                }
            }
        return (vesselDifference + voyageDifference) / (2*numberOfOrders);
    }

    private ArrayList<Individual> getnClosest(Individual individual, int nClose){
        ArrayList<Individual> nClosest = new ArrayList<Individual>();
        ArrayList<Map.Entry<Individual, Double>> otherIndividuals = new ArrayList<Map.Entry<Individual, Double>>(hammingDistances.get(individual).entrySet());
        Collections.sort(otherIndividuals, Utilities.getMapEntryWithDoubleComparator());
        for (int i = 0; i < nClose; i++){
            nClosest.add(otherIndividuals.get(i).getKey());
        }
        return nClosest;
    }

    public void setPenalizedCostIndividual(Individual individual, double durationViolationPenalty, double capacityViolationPenalty, double deadlineViolationPenalty) {
        double penalizedCost = individual.getScheduleCost() + individual.getDurationViolation()*durationViolationPenalty + individual.getCapacityViolation()*capacityViolationPenalty+ individual.getDeadlineViolation()*deadlineViolationPenalty;
        penalizedCost = Math.round(penalizedCost);
        individual.setPenalizedCost(penalizedCost);

    }

    @Override
    public HashMap<Integer,Node> getSolutionNodes(Individual individual) {
        return null;
    }


    public void setPenalizedCostIndividual(Individual individual) {
        setPenalizedCostIndividual(individual, durationViolationPenalty, capacityViolationPenalty, deadlineViolationPenalty);
    }

    public double getPenalizedCost(ArrayList<Integer> orderSequence) {
        return 0;
    }

    public double getPenalizedCost(ArrayList<Integer> orderSequence, double durationViolationPenalty, double capacityViolationPenalty) {
        return 0;
    }

    public double getPenalizedCostOfVoyage(ArrayList<Integer> orderSequence, int vessel) {
        return getPenalizedCostOfVoyage(orderSequence, vessel, durationViolationPenalty, capacityViolationPenalty, deadlineViolationPenalty);
    }

    public double getPenalizedCostOfVoyage(ArrayList<Integer> orderSequence, int vessel, double durationViolationPenalty, double capacityViolationPenalty, double deadlineViolationPenalty) {
        return 0;
    }

    public double getDurationViolationPenalty() {
        return durationViolationPenalty;
    }

    public double getCapacityViolationPenalty() {
        return capacityViolationPenalty;
    }

    public double getDeadlineViolationPenalty() {
        return deadlineViolationPenalty;
    }

    public void setDurationViolationPenalty(double durationViolationPenalty) {
        this.durationViolationPenalty = durationViolationPenalty;
    }

    public void setCapacityViolationPenalty(double capacityViolationPenalty) {
        this.capacityViolationPenalty = capacityViolationPenalty;
    }

    public void setDeadlineViolationPenalty(double deadlineViolationPenalty) {
        this.deadlineViolationPenalty = deadlineViolationPenalty;
    }

    public void setPenalizedCostPopulation(ArrayList<Individual> population) {

    }

}
