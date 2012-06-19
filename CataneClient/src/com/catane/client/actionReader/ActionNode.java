package com.catane.client.actionReader;

import java.util.ArrayList;
import java.util.HashMap;

import com.catane.client.actions.Action;

public class ActionNode {

	private int father;
	private int fson;
	private int psib;
	private int nsib;

	private ArrayList<Action> actions;
	private static HashMap<Integer, ActionNode> nodes = new HashMap<Integer, ActionNode>();	
	public ActionNode(int id){
		actions = new ArrayList<Action>();
		nodes.put(id, this);
	}
	
	public void addAction(Action a){
		actions.add(a);
	}
	
	public int getNbActions(){
		return actions.size();
	}
	
	public Action getAction(int i){
		return actions.get(i);
	}

	public ActionNode getFather() {
		return nodes.get(father);
	}

	public void setFather(int father) {
		this.father = father;
	}

	public ActionNode getFson() {
		return nodes.get(fson);
	}

	public void setFson(int fson) {
		this.fson = fson;
	}

	public ActionNode getPsib() {
		return nodes.get(psib);
	}

	public void setPsib(int psib) {
		this.psib = psib;
	}

	public ActionNode getNsib() {
		return nodes.get(nsib);
	}

	public void setNsib(int nsib) {
		this.nsib = nsib;
	}
	
	
}
