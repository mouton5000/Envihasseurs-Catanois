package com.catane.client.map;


final class HexagonePath extends PionPath{

	/**
	 * Longueur d'un côté d'un hexagone.
	 */
	public static final int HEXAGONES_SIDE_LENGTH = 100;
	
	/**
	 * Soit A le sommet gauche de l'hexagone, et B le sommet gauche d'un des deux côté horizontaux
	 * de l'hexagone. Soit enfin C l'instersection de l'horizontale passant par A et la verticale
	 * passant par B, alors HLARGEUR est égale à la longueur du segment [AC]
	 */
	public static final int HLARGEUR = HEXAGONES_SIDE_LENGTH/2;
	
	/**
	 * Soit A le sommet gauche de l'hexagone, et B le sommet gauche d'un des deux côté horizontaux
	 * de l'hexagone. Soit enfin C l'instersection de l'horizontale passant par A et la verticale
	 * passant par B, alors HLONGUEUR est égale à la longueur du segment [BC]
	 */
	public static final int HLONGUEUR = (int)(Math.sqrt(3) * (HEXAGONES_SIDE_LENGTH/2));
	
	
	private HexagoneInfos infos;
	
	/**
	 * Construit un hexagone horizontal (un segment horizontal au dessus et un autre
	 * en dessous, à gauche et à droite, 2 segments obliques) dont le point gauche
	 * du segment horizontal du dessus est en x,y. La taille est définie par le zoom
	 * actuel de la carte et par le nombre HEXAGONES_WIDTH.
	 * @param x
	 * @param y
	 * @return Ce shapeBuilder, pour pouvoir aligner les appels de méthodes.
	 */
	public HexagonePath(int x, int y) {
		super(x-HLARGEUR, y-HLONGUEUR);
		this.lineRelativelyTo(2*HLARGEUR,0);
		this.lineRelativelyTo(HLARGEUR,HLONGUEUR);
		this.lineRelativelyTo(-HLARGEUR,HLONGUEUR);
		this.lineRelativelyTo(-2*HLARGEUR,0);
		this.lineRelativelyTo(-HLARGEUR,-HLONGUEUR);
		this.close();
	}

	public HexagoneInfos getInfos() {
		return infos;
	}

	public void setInfos(HexagoneInfos infos) {
		this.infos = infos;
	}
	
	public int[] getCoords(){
		int[] c = {this.getX()+HLARGEUR,this.getY()+HLONGUEUR};
		return c;
	}
	

}
