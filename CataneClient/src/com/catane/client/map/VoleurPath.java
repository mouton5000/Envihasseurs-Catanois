package com.catane.client.map;

public abstract class VoleurPath extends PionPath{

	public VoleurPath() {
		super(0,0);
		// TODO Auto-generated constructor stub
	}

}

class BrigandPath extends VoleurPath {


	public static final double BRIGAND_WIDTHR = 0.50;
	public static final double BRIGAND_HEIGHTR = 1.00;
	
	public static final int w = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*BRIGAND_WIDTHR);
	public static final int h = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*BRIGAND_HEIGHTR);
	
	/**
	 * Renvoie un chemin qui dessine un bigand centré en l'origine.
	 */
	public BrigandPath() {
		super();
		
		this.lineRelativelyTo(w/4,-h/4);
		this.curveRelativelyTo(
				-(w*6)/10,-h*6/7, 
				w/2+(w*6)/10,-h*6/7, 
				w/2,0);
		this.lineRelativelyTo(w/4,h/4);
		this.close();
	}
	
	public void setX(int x){
		super.setX((int)(x-w*0.5));
	}
	
	public void setY(int y){
		super.setY((int)(y+h*0.4));
	}
	

}


class PiratePath extends VoleurPath {

	
	public static final double PIRATE_WIDTHR = 0.90;
	public static final double PIRATE_HEIGHTR = 0.90;
	
	public static final int w = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*PIRATE_WIDTHR);
	public static final int h = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*PIRATE_HEIGHTR);
	
	/**
	 * Renvoie un chemin qui dessine un pirate centré en l'origine.
	 */
	public PiratePath() {
		super();
		this.lineRelativelyTo(w*4/10, 0);
		this.lineRelativelyTo(0, -h*4/10);
		this.lineRelativelyTo(w*3/10, 0);
		this.lineRelativelyTo(0, h*2/10);
		this.lineRelativelyTo(-w*2/10, 0);
		this.lineRelativelyTo(0, h*2/10);
		this.lineRelativelyTo(w*5/10, 0);
		this.curveRelativelyTo(
				-w/4,h*4/10, 
				-w*3/4,h*4/10,
				-w,0);
		this.close();
	}
	
	
	public void setX(int x){
		super.setX((int)(x-w*0.5));
	}
}
