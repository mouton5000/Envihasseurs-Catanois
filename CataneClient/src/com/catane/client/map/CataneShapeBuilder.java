package com.catane.client.map;

import gwt.g2d.client.graphics.shapes.ShapeBuilder;
import gwt.g2d.client.math.Vector2;

class CataneShapeBuilder extends ShapeBuilder{

	/**
	 * Longueur d'un côté d'un hexagone.
	 */
	public static final int HEXAGONES_SIDE_LENGTH = 100;
	
	/**
	 * Soit A le sommet gauche de l'hexagone, et B le sommet gauche d'un des deux côté horizontaux
	 * de l'hexagone. Soit enfin C l'instersection de l'horizontale passant par A et la verticale
	 * passant par B, alors HLARGEUR est égale à la longueur du segment [AC]
	 */
	public static final double HLARGEUR = HEXAGONES_SIDE_LENGTH/2.0;
	
	/**
	 * Soit A le sommet gauche de l'hexagone, et B le sommet gauche d'un des deux côté horizontaux
	 * de l'hexagone. Soit enfin C l'instersection de l'horizontale passant par A et la verticale
	 * passant par B, alors HLONGUEUR est égale à la longueur du segment [BC]
	 */
	public static final double HLONGUEUR = Math.sqrt(3) * HEXAGONES_SIDE_LENGTH/2.0;


	public CataneShapeBuilder() {
		super();
	}


	
	/**
	 * Dessine un hexagone horizontal (un segment horizontal au dessus et un autre
	 * en dessous, à gauche et à droite, 2 segments obliques) dont le point gauche
	 * du segment horizontal du dessus est en x,y. La taille est définie par le zoom
	 * actuel de la carte et par le nombre HEXAGONES_WIDTH.
	 * @param x
	 * @param y
	 * @return Ce shapeBuilder, pour pouvoir aligner les appels de méthodes.
	 */
	public CataneShapeBuilder drawHexagone(double x, double y){

		this.translate(-HLARGEUR, -HLONGUEUR)
		.moveTo(x,y)
		.drawLineTo(x+HEXAGONES_SIDE_LENGTH, y)
		.drawLineTo(x+HEXAGONES_SIDE_LENGTH+HLARGEUR, y+HLONGUEUR)
		.drawLineTo(x+HEXAGONES_SIDE_LENGTH, y+2*HLONGUEUR)
		.drawLineTo(x, y+2*HLONGUEUR)
		.drawLineTo(x - HLARGEUR, y+HLONGUEUR)
		.drawLineTo(x, y)
		.translate(HLARGEUR, HLONGUEUR);

		
		return this;
	}



	public static final double COLONIE_HEIGHTR = 0.17;
	public static final double COLONIE_WIDTHR = 0.20;

	/**
	 * Dessine une colonie à l'emplacement x, y. (x,y) se retrouve au
	 * centre de la colonie.
	 * @param x
	 * @param y
	 * @return Ce shapeBuilder, pour pouvoir aligner les appels de méthodes.
	 */
	public CataneShapeBuilder drawColonie(double x, double y){
		int w = (int)(HEXAGONES_SIDE_LENGTH * COLONIE_WIDTHR);
		int h = (int)(HEXAGONES_SIDE_LENGTH * COLONIE_HEIGHTR);
		
		this
		.translate(-w/2, h/2)
		.moveTo(x,y)
		.drawLineTo(x,y-h)
		.drawLineTo(x+w/2,y-3*h/2)
		.drawLineTo(x+w,y-h)
		.drawLineTo(x+w,y)
		.drawLineTo(x, y)
		.translate(w/2, -h/2);
		return this;
	}

	public static final double VILLE_HEIGHTR = 0.25;
	public static final double VILLE_WIDTHR = 0.20;

	/**
	 * Dessine une ville à l'emplacement x, y. (x,y) se retrouve au
	 * centre de la ville.
	 * @param x
	 * @param y
	 * @return Ce shapeBuilder, pour pouvoir aligner les appels de méthodes.
	 */
	public CataneShapeBuilder drawVille(double x, double y){
		int w = (int)(HEXAGONES_SIDE_LENGTH * VILLE_WIDTHR);
		int h = (int)(HEXAGONES_SIDE_LENGTH * VILLE_HEIGHTR);
		
		this
		.translate(-w/3, h/3)
		.moveTo(x,y)
		.drawLineTo(x,y-7*h/8)
		.drawLineTo(x+w/4,y-h*(13.0/12))
		.drawLineTo(x+w/2,y-7*h/8)
		.drawLineTo(x+w/2,y-h*(7.0/12))
		.drawLineTo(x+w,y-h*(7.0/12))
		.drawLineTo(x+w,y)
		.drawLineTo(x, y)
		.translate(w/3, -h/3);
		return this;
	}

	public static final double ROUTE_WIDTHR = 0.15;
	public static final double ROUTE_OFFSETR = 0.20;

	/**
	 * Dessine une route entre les emplacements x0, y0 et x1,y1.
	 * La route est légèrement décalée par rapport à ses deux extrêmités.
	 * @param x0
	 * @param y0
	 * @param x1
	 * @param y1
	 * @return Ce shapeBuilder, pour pouvoir aligner les appels de méthodes.
	 */
	public CataneShapeBuilder drawRoute(double x0, double y0, double x1, double y1){
		
		int w = (int)(HEXAGONES_SIDE_LENGTH * ROUTE_WIDTHR);
		int off = (int)(HEXAGONES_SIDE_LENGTH * ROUTE_OFFSETR);
		
		
		// Calcul des vecteurs unitaires de la droite relaint N (x0,y0) et M (x1, y1), et sa droite
		// orthogonale.
		Vector2 nm = new Vector2(x1 - x0,y1 - y0);
		Vector2 u = nm.normalize();
		Vector2 v = new Vector2(u.getY(), -u.getX());

		/*
		 * Si on observe la route à l'horizontale avec N0 à gauche et N1 à droite
		 * N00 est le point en bas à gauche
		 * N01 est le point en haut à gauche
		 * N11 est le point en haut à droite
		 * N10 est le point en base à droite
		 */

		double x00 =x0+u.getX()*off-v.getX()*w/2; 
		double y00 =y0+u.getY()*off-v.getY()*w/2;
		double height = nm.length() - 2*off;

		double x01 =x00+v.getX()*w; 
		double y01 =y00+v.getY()*w;

		double x11 =x01+u.getX()*height;
		double y11 =y01+u.getY()*height;

		double x10 =x11-v.getX()*w;
		double y10 =y11-v.getY()*w;

		this
		.moveTo(x00,y00)
		.drawLineTo(x01,y01)
		.drawLineTo(x11,y11)
		.drawLineTo(x10,y10)
		.drawLineTo(x00,y00);
		return this;
	}

	public static final double BATEAU_HEIGHTR = 0.10;
	public static final double BATEAU_OFFSETR = 0.33;

	
	
	/**
	 * Dessine un bateau entre les emplacements N0 (x0,y0) et N1 (x1,y1).
	 * @param x0
	 * @param y0
	 * @param x1
	 * @param y1
	 * @return
	 */
	public CataneShapeBuilder drawBateauTransport(double x0, double y0, double x1, double y1){

		// On place N0 à gauche de N1.
		if(x1 < x0){
			double swap = x0;
			x0 = x1;
			x1 = swap;

			swap = y0;
			y0 = y1;
			y1 = swap;
		}

		// Calcul des vecteurs unitaires de la droite relaint N (x0,y0) et M (x1, y1), et sa droite
		// orthogonale.
		Vector2 nm = new Vector2(x1 - x0,y1 - y0);
		Vector2 u = nm.normalize();
		Vector2 v = new Vector2(u.getY(), -u.getX());

		int h = (int)(HEXAGONES_SIDE_LENGTH*BATEAU_HEIGHTR);
		double offset = nm.length()*BATEAU_OFFSETR;
		
		// bord gauche
		double x00 =x0+u.getX()*offset; 
		double y00 =y0+u.getY()*offset;
		double w = nm.length() - 2*offset;

		double x01 =x00+v.getX()*h/4.0; 
		double y01 =y00+v.getY()*h/4.0;

		// Coordonnées du mat
		double xm1 =x01+u.getX()*w*0.4;
		double ym1 =y01+u.getY()*w*0.4;
		
		double xm2 =xm1+v.getX()*h;
		double ym2 =ym1+v.getY()*h;
		
		double xm3 =xm2+u.getX()*w*0.3-v.getX()*h*0.5 ;
		double ym3 =ym2+u.getY()*w*0.3-v.getY()*h*0.5;
		
		double xm5 =x01+u.getX()*w*0.525;
		double ym5 =y01+u.getY()*w*0.525;
		
		double xm4 =xm5+v.getX()*h*0.25;
		double ym4 =ym5+v.getY()*h*0.25;
		
		// bord droit
		double x11 =x01+u.getX()*w;
		double y11 =y01+u.getY()*w;

		double x10 =x11-v.getX()*h/4.0;
		double y10 =y11-v.getY()*h/4.0;
		
		// Coordonée basse du bateau
		double xb = x00+u.getX()*w*0.5 - v.getX()*h*2;
		double yb = y00+u.getY()*w*0.5 - v.getY()*h*2;
		
		
		this
		.moveTo(x00,y00)
		.drawLineTo(x01, y01)
		.drawLineTo(xm1,ym1)
		.drawLineTo(xm2,ym2)
		.drawLineTo(xm3,ym3)
		.drawLineTo(xm4,ym4)
		.drawLineTo(xm5,ym5)
		.drawLineTo(x11,y11)
		.drawLineTo(x10,y10)
		.drawArcTo(xb,yb,x00,y00,2*h);
		return this;
	}

	public static final double CARGO_HEIGHTR = 0.10;
	public static final double CARGO_OFFSETR = 0.23;

	
	
	/**
	 * Dessine un bateau entre les emplacements N0 (x0,y0) et N1 (x1,y1).
	 * @param x0
	 * @param y0
	 * @param x1
	 * @param y1
	 * @return
	 */
	public CataneShapeBuilder drawCargo(double x0, double y0, double x1, double y1){

		// On place N0 à gauche de N1.
		if(x1 < x0){
			double swap = x0;
			x0 = x1;
			x1 = swap;

			swap = y0;
			y0 = y1;
			y1 = swap;
		}

		// Calcul des vecteurs unitaires de la droite relaint N (x0,y0) et M (x1, y1), et sa droite
		// orthogonale.
		Vector2 nm = new Vector2(x1 - x0,y1 - y0);
		Vector2 u = nm.normalize();
		Vector2 v = new Vector2(u.getY(), -u.getX());

		int h = (int)(HEXAGONES_SIDE_LENGTH*CARGO_HEIGHTR);
		double offset = nm.length()*CARGO_OFFSETR;
		
		// bord gauche
		double x00 =x0+u.getX()*offset; 
		double y00 =y0+u.getY()*offset;
		double w = nm.length() - 2*offset;

		double x01 =x00+v.getX()*h/4.0; 
		double y01 =y00+v.getY()*h/4.0;

		// Coordonnées du mat
		double xm1 =x01+u.getX()*w*0.4;
		double ym1 =y01+u.getY()*w*0.4;
		
		double xm2 =xm1+v.getX()*h;
		double ym2 =ym1+v.getY()*h;
		
		double xm3 =xm2+u.getX()*w*0.25-v.getX()*h*0.5 ;
		double ym3 =ym2+u.getY()*w*0.25-v.getY()*h*0.5;
		
		double xm5 =x01+u.getX()*w*0.5;
		double ym5 =y01+u.getY()*w*0.5;
		
		double xm4 =xm5+v.getX()*h*0.25;
		double ym4 =ym5+v.getY()*h*0.25;
		
		// bord droit
		double x11 =x01+u.getX()*w;
		double y11 =y01+u.getY()*w;

		double x10 =x11-v.getX()*h/4.0;
		double y10 =y11-v.getY()*h/4.0;
		
		// Coordonée basse du CARGO
		double xb = x00+u.getX()*w*0.5 - v.getX()*h*2;
		double yb = y00+u.getY()*w*0.5 - v.getY()*h*2;
		
		
		this
		.moveTo(x00,y00)
		.drawLineTo(x01, y01)
		.drawLineTo(xm1,ym1)
		.drawLineTo(xm2,ym2)
		.drawLineTo(xm3,ym3)
		.drawLineTo(xm4,ym4)
		.drawLineTo(xm5,ym5)
		.drawLineTo(x11,y11)
		.drawLineTo(x10,y10)
		.drawArcTo(xb,yb,x00,y00,4*h);
		return this;
	}

	public static final double VOILLIER_HEIGHTR = 0.10;
	public static final double VOILLIER_OFFSET_RATIO = 0.23;

	
	
	/**
	 * Dessine un bateau entre les emplacements N0 (x0,y0) et N1 (x1,y1).
	 * @param x0
	 * @param y0
	 * @param x1
	 * @param y1
	 * @return
	 */
	public CataneShapeBuilder drawVoillier(double x0, double y0, double x1, double y1){

		// On place N0 à gauche de N1.
		if(x1 < x0){
			double swap = x0;
			x0 = x1;
			x1 = swap;

			swap = y0;
			y0 = y1;
			y1 = swap;
		}

		// Calcul des vecteurs unitaires de la droite relaint N (x0,y0) et M (x1, y1), et sa droite
		// orthogonale.
		Vector2 nm = new Vector2(x1 - x0,y1 - y0);
		Vector2 u = nm.normalize();
		Vector2 v = new Vector2(u.getY(), -u.getX());

		int h = (int)(HEXAGONES_SIDE_LENGTH*VOILLIER_HEIGHTR);
		double offset = nm.length()*VOILLIER_OFFSET_RATIO;
		
		// bord gauche
		double x00 =x0+u.getX()*offset; 
		double y00 =y0+u.getY()*offset;
		double w = nm.length() - 2*offset;

		double x01 =x00+v.getX()*h/4.0; 
		double y01 =y00+v.getY()*h/4.0;

		// Coordonnées du mat 1
		double xm11 =x01+u.getX()*w*0.2;
		double ym11 =y01+u.getY()*w*0.2;
		
		double xm12 =xm11+v.getX()*h;
		double ym12 =ym11+v.getY()*h;
		
		double xm13 =xm12+u.getX()*w*0.25-v.getX()*h*0.5 ;
		double ym13 =ym12+u.getY()*w*0.25-v.getY()*h*0.5;
		
		double xm15 =x01+u.getX()*w*0.3;
		double ym15 =y01+u.getY()*w*0.3;
		
		double xm14 =xm15+v.getX()*h*0.25;
		double ym14 =ym15+v.getY()*h*0.25;

		// Coordonnées du mat 1
		double xm21 =x01+u.getX()*w*0.6;
		double ym21 =y01+u.getY()*w*0.6;
		
		double xm22 =xm21+v.getX()*h;
		double ym22 =ym21+v.getY()*h;
		
		double xm23 =xm22+u.getX()*w*0.25-v.getX()*h*0.5 ;
		double ym23 =ym22+u.getY()*w*0.25-v.getY()*h*0.5;
		
		double xm25 =x01+u.getX()*w*0.7;
		double ym25 =y01+u.getY()*w*0.7;
		
		double xm24 =xm25+v.getX()*h*0.25;
		double ym24 =ym25+v.getY()*h*0.25;
		
		// bord droit
		double x11 =x01+u.getX()*w;
		double y11 =y01+u.getY()*w;

		double x10 =x11-v.getX()*h/4.0;
		double y10 =y11-v.getY()*h/4.0;
		
		// Coordonée basse du VOILLIER
		double xb = x00+u.getX()*w*0.5 - v.getX()*h*2;
		double yb = y00+u.getY()*w*0.5 - v.getY()*h*2;
		
		
		this
		.moveTo(x00,y00)
		.drawLineTo(x01, y01)
		.drawLineTo(xm11,ym11)
		.drawLineTo(xm12,ym12)
		.drawLineTo(xm13,ym13)
		.drawLineTo(xm14,ym14)
		.drawLineTo(xm15,ym15)
		.drawLineTo(xm21,ym21)
		.drawLineTo(xm22,ym22)
		.drawLineTo(xm23,ym23)
		.drawLineTo(xm24,ym24)
		.drawLineTo(xm25,ym25)
		.drawLineTo(x11,y11)
		.drawLineTo(x10,y10)
		.drawArcTo(xb,yb,x00,y00,4*h);
		return this;
	}
	
	public static final double BRIGAND_WIDTHR = 0.50;
	public static final double BRIGAND_HEIGHTR = 1.00;
	public CataneShapeBuilder drawBrigand(double x, double y){
		
		int w = (int)(HEXAGONES_SIDE_LENGTH*BRIGAND_WIDTHR);
		int h = (int)(HEXAGONES_SIDE_LENGTH*BRIGAND_HEIGHTR);
		
		this
		.cTranslate(-w*0.5, h*0.40)
		.cMoveTo(x, y)
		.drawLineTo(x+w*0.25,y-h*0.25)
		.drawBezierCurveTo(
				x-w*0.3,y-h*1, 
				x+w*1.3,y-h*1, 
				x+w*0.75,y-h*0.25)
		.drawLineTo(x+w,y)
		.drawLineTo(x,y);
		this.cTranslate(w*0.5, -h*0.40);
		return this;
	}
	
	
	public static final double PIRATE_WIDTHR = 0.90;
	public static final double PIRATE_HEIGHTR = 0.90;
	
	/**
	 * Dessine un bateau entre les emplacements N0 (x0,y0) et N1 (x1,y1).
	 * @param x0
	 * @param y0
	 * @param x1
	 * @param y1
	 * @return
	 */
	public CataneShapeBuilder drawPirate(double x, double y){
		
		int w = (int)(HEXAGONES_SIDE_LENGTH*PIRATE_WIDTHR);
		int h = (int)(HEXAGONES_SIDE_LENGTH*PIRATE_HEIGHTR);
				
		this
		.cTranslate(-w/2.0, 0)
		.cMoveTo(x,y)
		.drawLineTo(x+w*0.4, y)
		.drawLineTo(x+w*0.4,y-h*0.4)
		.drawLineTo(x+w*0.7,y-h*0.4)
		.drawLineTo(x+w*0.7,y-h*0.2)
		.drawLineTo(x+w*0.5,y-h*0.2)
		.drawLineTo(x+w*0.5,y)
		.drawLineTo(x+w,y)
		.drawBezierCurveTo(
				x+w*0.75,y+0.4*h, 
				x+w*0.25,y+0.4*h, 
				x,y);
		this.cTranslate(w/2.0, 0);
		
		return this;
	}
	
	public CataneShapeBuilder cTranslate(double x, double y){
		super.translate(x, y);
		return this;
	}

	public CataneShapeBuilder cMoveTo(double x, double y){
		super.moveTo(x, y);
		return this;
	}

	public CataneShapeBuilder cScale(double sc){
		super.scale(sc);
		return this;
	}
}


