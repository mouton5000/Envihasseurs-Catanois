package com.catane.client.map;

import java.util.ArrayList;

import org.vaadin.gwtgraphics.client.Group;
import org.vaadin.gwtgraphics.client.VectorObject;
import org.vaadin.gwtgraphics.client.shape.Circle;
import org.vaadin.gwtgraphics.client.shape.Path;
import org.vaadin.gwtgraphics.client.shape.Rectangle;
import org.vaadin.gwtgraphics.client.shape.Text;

public abstract class PionsJoueursGroup extends Group{

	private ArrayList<Integer> joueurs;

	private Text nbPions;
	private Circle circNbPions;
	private Rectangle rectNbPions;
	private Path modelPion;
	
	private static final int textOffSet = 15;
	
	public PionsJoueursGroup(ArrayList<Integer> joueurs) {
		super();
		this.setJoueurs(joueurs);
		nbPions = new Text(textOffSet, textOffSet, String.valueOf(joueurs.size()));
		nbPions.setFillColor("black");
		
		int tw = nbPions.getTextWidth();
		int th = nbPions.getTextHeight()-6;
		int x0 = textOffSet + tw/2;
		int y0 = textOffSet - th/2+1;
		int r = (int)(Math.sqrt(tw*tw/4 + th*th/4));
		circNbPions = new Circle(x0,y0,r);
		circNbPions.setFillColor("white");
		rectNbPions = new Rectangle(textOffSet, textOffSet-th, tw, th);
		rectNbPions.setFillColor("white");
		super.add(circNbPions);
		super.add(nbPions);
	}
	
	@Override
	public VectorObject add(VectorObject vo) {
		VectorObject v = super.add(vo);
		this.bringToFront(circNbPions);
		this.bringToFront(nbPions);
		return v;
	}

	public ArrayList<Integer> getJoueurs() {
		return joueurs;
	}

	public void setJoueurs(ArrayList<Integer> joueurs) {
		this.joueurs = joueurs;
	}

	public void setModelPion(Path modelPion) {
		this.add(modelPion);
		this.modelPion = modelPion;
	}
	
	public void setX(int x){
		int delta = x-modelPion.getX();
		modelPion.setX(x);
		circNbPions.setX(circNbPions.getX()+delta);
		nbPions.setX(nbPions.getX()+delta);
	}
	
	public void setY(int y){
		int delta = y-modelPion.getY();
		modelPion.setY(y);
		circNbPions.setY(circNbPions.getY()+delta);
		nbPions.setY(nbPions.getY()+delta);
	}
	
	public void setFillColor(String color){
		modelPion.setFillColor(color);
	}

	public void setFillOpacity(double opacity) {
		modelPion.setFillOpacity(opacity);
	}

}

class BateauxGroup extends PionsJoueursGroup{

	public static final double BATEAU_HEIGHTR = 0.10;
	public static final double BATEAU_OFFSETR = 0.33;

	public static final int h = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*BATEAU_HEIGHTR);
	public static final int off = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH * BATEAU_OFFSETR);
	
	public BateauxGroup(ArrayList<Integer> joueurs, SideDirection dir) {
		super(joueurs);
		Path bateau = new Path(0,0);
		PionBuilder.makeTransport(bateau, h, off, dir);
		this.setModelPion(bateau);
		
	}
	
	
	
}
