package com.catane.client.map;

import gwt.g2d.client.math.Vector2;

import org.vaadin.gwtgraphics.client.shape.Path;

class PionBuilder {

	static void makeColonie(Path p, int w, int h){
		p.lineRelativelyTo(0, -h);
		p.lineRelativelyTo(w/2, -h/2);
		p.lineRelativelyTo(w/2, h/2);
		p.lineRelativelyTo(0, h);
		p.close();
	}

	static void makeVille(Path p, int w, int h){
		p.lineRelativelyTo(0, -h*7/8);
		p.lineRelativelyTo(w/4, -h*1/5);
		p.lineRelativelyTo(w/4, h*1/5);
		p.lineRelativelyTo(0, h*3/12);
		p.lineRelativelyTo(w/2, 0);
		p.lineRelativelyTo(0, h*15/24);
		p.close();
	}

	static void makeRoute(Path p, int w, int off, SideDirection dir){
		int x0=0, x1=0, y0 = 0, y1 = 0;

		switch(dir){
		case LEFT:
			x0 = -HexagonePath.HLARGEUR/2;
			x1 = HexagonePath.HLARGEUR/2;
			y0 = HexagonePath.HLONGUEUR/2;
			y1 = -HexagonePath.HLONGUEUR/2;
			break;
		case NONE:
			x0 = -HexagonePath.HLARGEUR;
			x1 = HexagonePath.HLARGEUR;
			y0 = y1 = 0;
			break;
		case RIGHT:
			x0 = -HexagonePath.HLARGEUR/2;
			x1 = HexagonePath.HLARGEUR/2;
			y0 = -HexagonePath.HLONGUEUR/2;
			y1 = HexagonePath.HLONGUEUR/2;
			break;
		}

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

		int x00 =(int)(x0+u.getX()*off-v.getX()*w/2); 
		int y00 =(int)(y0+u.getY()*off-v.getY()*w/2);
		int height = (int)(nm.length() - 2*off);

		int dx01 =(int)(v.getX()*w); 
		int dy01 =(int)(v.getY()*w);

		int dx11 =(int)(u.getX()*height);
		int dy11 =(int)(u.getY()*height);

		int dx10 =(int)(-v.getX()*w);
		int dy10 =(int)(-v.getY()*w);

		p.moveRelativelyTo(x00, y00);
		p.lineRelativelyTo(dx01,dy01);
		p.lineRelativelyTo(dx11,dy11);
		p.lineRelativelyTo(dx10,dy10);
		p.close();
	}

	static void makeTransport(Path p, int h, int off, SideDirection dir){
		int x0=0, x1=0, y0 = 0, y1 = 0;

		switch(dir){
		case LEFT:
			x0 = -HexagonePath.HLARGEUR/2;
			x1 = HexagonePath.HLARGEUR/2;
			y0 = HexagonePath.HLONGUEUR/2;
			y1 = -HexagonePath.HLONGUEUR/2;
			break;
		case NONE:
			x0 = -HexagonePath.HLARGEUR;
			x1 = HexagonePath.HLARGEUR;
			y0 = y1 = 0;
			break;
		case RIGHT:
			x0 = -HexagonePath.HLARGEUR/2;
			x1 = HexagonePath.HLARGEUR/2;
			y0 = -HexagonePath.HLONGUEUR/2;
			y1 = HexagonePath.HLONGUEUR/2;
			break;
		}

		// Calcul des vecteurs unitaires de la droite relaint N (x0,y0) et M (x1, y1), et sa droite
		// orthogonale.
		Vector2 nm = new Vector2(x1 - x0,y1 - y0);
		Vector2 u = nm.normalize();
		Vector2 v = new Vector2(u.getY(), -u.getX());


		// bord gauche
		int x00 =(int)(x0+u.getX()*off); 
		int y00 =(int)(y0+u.getY()*off);
		int w = (int)(nm.length() - 2*off);

		int dx01 =(int)(v.getX()*h/4); 
		int dy01 =(int)(v.getY()*h/4);

		// Coordonnées du mat
		int dxm1 =(int)(u.getX()*w*0.4);
		int dym1 =(int)(u.getY()*w*0.4);

		int dxm2 =(int)(v.getX()*h);
		int dym2 =(int)(v.getY()*h);

		int dxm3 =(int)(u.getX()*w*0.3-v.getX()*h*0.5) ;
		int dym3 =(int)(u.getY()*w*0.3-v.getY()*h*0.5);

		int dxm4 = (int)(-u.getX()*w*0.175 - v.getX()*h*0.25);
		int dym4 = (int)(-u.getY()*w*0.175 - v.getY()*h*0.25);

		int dxm5 =(int)(-v.getX()*h*0.25);
		int dym5 =(int)(-v.getY()*h*0.25);

		// bord droit
		int dx11 =(int)(u.getX()*w*0.475);
		int dy11 =(int)(u.getY()*w*0.475);

		int dx10 =(int)(-v.getX()*h/4.0);
		int dy10 =(int)(-v.getY()*h/4.0);

		// Coordonée basse du bateau
		int dxb1 = (int)(-u.getX()*w*0.25 - v.getX()*h*2);
		int dyb1 = (int)(-u.getY()*w*0.25 - v.getY()*h*2);
		int dxb2 = (int)(-u.getX()*w*0.75 - v.getX()*h*2);
		int dyb2 = (int)(-u.getY()*w*0.75 - v.getY()*h*2);
		int dx00 = (int)(-u.getX()*w);
		int dy00 = (int)(-u.getY()*w);


		p.moveRelativelyTo(x00,y00);
		p.lineRelativelyTo(dx01, dy01);
		p.lineRelativelyTo(dxm1,dym1);
		p.lineRelativelyTo(dxm2,dym2);
		p.lineRelativelyTo(dxm3,dym3);
		p.lineRelativelyTo(dxm4,dym4);
		p.lineRelativelyTo(dxm5,dym5);
		p.lineRelativelyTo(dx11,dy11);
		p.lineRelativelyTo(dx10,dy10);
		p.curveRelativelyTo(dxb1,dyb1,dxb2,dyb2,dx00,dy00);
		p.close();
	}
	
	static void makeCargo(Path p, int h, int off, SideDirection dir){
int x0=0, x1=0, y0 = 0, y1 = 0;
		
		switch(dir){
		case LEFT:
			x0 = -HexagonePath.HLARGEUR/2;
			x1 = HexagonePath.HLARGEUR/2;
			y0 = HexagonePath.HLONGUEUR/2;
			y1 = -HexagonePath.HLONGUEUR/2;
			break;
		case NONE:
			x0 = -HexagonePath.HLARGEUR;
			x1 = HexagonePath.HLARGEUR;
			y0 = y1 = 0;
			break;
		case RIGHT:
			x0 = -HexagonePath.HLARGEUR/2;
			x1 = HexagonePath.HLARGEUR/2;
			y0 = -HexagonePath.HLONGUEUR/2;
			y1 = HexagonePath.HLONGUEUR/2;
			break;
		}

				// Calcul des vecteurs unitaires de la droite relaint N (x0,y0) et M (x1, y1), et sa droite
				// orthogonale.
				Vector2 nm = new Vector2(x1 - x0,y1 - y0);
				Vector2 u = nm.normalize();
				Vector2 v = new Vector2(u.getY(), -u.getX());

				
				// bord gauche
				int x00 =(int)(x0+u.getX()*off); 
				int y00 =(int)(y0+u.getY()*off);
				int w = (int)(nm.length() - 2*off);

				int dx01 =(int)(v.getX()*h/4); 
				int dy01 =(int)(v.getY()*h/4);

				// Coordonnées du mat
				int dxm1 =(int)(u.getX()*w*0.4);
				int dym1 =(int)(u.getY()*w*0.4);
				
				int dxm2 =(int)(v.getX()*h);
				int dym2 =(int)(v.getY()*h);
				
				int dxm3 =(int)(u.getX()*w*0.3-v.getX()*h*0.5) ;
				int dym3 =(int)(u.getY()*w*0.3-v.getY()*h*0.5);
				
				int dxm4 = (int)(-u.getX()*w*0.175 - v.getX()*h*0.25);
				int dym4 = (int)(-u.getY()*w*0.175 - v.getY()*h*0.25);
				
				int dxm5 =(int)(-v.getX()*h*0.25);
				int dym5 =(int)(-v.getY()*h*0.25);
				
				// bord droit
				int dx11 =(int)(u.getX()*w*0.475);
				int dy11 =(int)(u.getY()*w*0.475);

				int dx10 =(int)(-v.getX()*h/4.0);
				int dy10 =(int)(-v.getY()*h/4.0);
				
				// Coordonée basse du bateau
				int dxb1 = (int)(-u.getX()*w*0.25 - v.getX()*h*2);
				int dyb1 = (int)(-u.getY()*w*0.25 - v.getY()*h*2);
				int dxb2 = (int)(-u.getX()*w*0.75 - v.getX()*h*2);
				int dyb2 = (int)(-u.getY()*w*0.75 - v.getY()*h*2);
				int dx00 = (int)(-u.getX()*w);
				int dy00 = (int)(-u.getY()*w);
				
				
				p.moveRelativelyTo(x00,y00);
				p.lineRelativelyTo(dx01, dy01);
				p.lineRelativelyTo(dxm1,dym1);
				p.lineRelativelyTo(dxm2,dym2);
				p.lineRelativelyTo(dxm3,dym3);
				p.lineRelativelyTo(dxm4,dym4);
				p.lineRelativelyTo(dxm5,dym5);
				p.lineRelativelyTo(dx11,dy11);
				p.lineRelativelyTo(dx10,dy10);
				p.curveRelativelyTo(dxb1,dyb1,dxb2,dyb2,dx00,dy00);
				p.close();
	}
	
	static void makeVoilier(Path p, int h, int off, SideDirection dir){
int x0=0, x1=0, y0 = 0, y1 = 0;
		
		switch(dir){
		case LEFT:
			x0 = -HexagonePath.HLARGEUR/2;
			x1 = HexagonePath.HLARGEUR/2;
			y0 = HexagonePath.HLONGUEUR/2;
			y1 = -HexagonePath.HLONGUEUR/2;
			break;
		case NONE:
			x0 = -HexagonePath.HLARGEUR;
			x1 = HexagonePath.HLARGEUR;
			y0 = y1 = 0;
			break;
		case RIGHT:
			x0 = -HexagonePath.HLARGEUR/2;
			x1 = HexagonePath.HLARGEUR/2;
			y0 = -HexagonePath.HLONGUEUR/2;
			y1 = HexagonePath.HLONGUEUR/2;
			break;
		}

				// Calcul des vecteurs unitaires de la droite relaint N (x0,y0) et M (x1, y1), et sa droite
				// orthogonale.
				Vector2 nm = new Vector2(x1 - x0,y1 - y0);
				Vector2 u = nm.normalize();
				Vector2 v = new Vector2(u.getY(), -u.getX());
				
				// bord gauche
				int x00 =(int)(x0+u.getX()*off); 
				int y00 =(int)(y0+u.getY()*off);
				int w = (int)(nm.length() - 2*off);

				int dx01 =(int)(v.getX()*h/4); 
				int dy01 =(int)(v.getY()*h/4);

				// Coordonnées du mat 1
				int dxm11 =(int)(u.getX()*w*0.225);
				int dym11 =(int)(u.getY()*w*0.225);
				
				int dxm12 =(int)(v.getX()*h);
				int dym12 =(int)(v.getY()*h);
				
				int dxm13 =(int)(u.getX()*w*0.3-v.getX()*h*0.5) ;
				int dym13 =(int)(u.getY()*w*0.3-v.getY()*h*0.5);
				
				int dxm14 = (int)(-u.getX()*w*0.175 - v.getX()*h*0.25);
				int dym14 = (int)(-u.getY()*w*0.175 - v.getY()*h*0.25);
				
				int dxm15 =(int)(-v.getX()*h*0.25);
				int dym15 =(int)(-v.getY()*h*0.25);
				
				
				// Coordonnées du mat 2
				int dxm21 =(int)(u.getX()*w*0.3);
				int dym21 =(int)(u.getY()*w*0.3);
				
				int dxm22 =(int)(v.getX()*h);
				int dym22 =(int)(v.getY()*h);
				
				int dxm23 =(int)(u.getX()*w*0.3-v.getX()*h*0.5) ;
				int dym23 =(int)(u.getY()*w*0.3-v.getY()*h*0.5);
				
				int dxm24 = (int)(-u.getX()*w*0.175 - v.getX()*h*0.25);
				int dym24 = (int)(-u.getY()*w*0.175 - v.getY()*h*0.25);
				
				int dxm25 =(int)(-v.getX()*h*0.25);
				int dym25 =(int)(-v.getY()*h*0.25);
				
				// bord droit
				int dx11 =(int)(u.getX()*w*0.225);
				int dy11 =(int)(u.getY()*w*0.225);

				int dx10 =(int)(-v.getX()*h/4.0);
				int dy10 =(int)(-v.getY()*h/4.0);
				
				// Coordonée basse du bateau
				int dxb1 = (int)(-u.getX()*w*0.25 - v.getX()*h*2);
				int dyb1 = (int)(-u.getY()*w*0.25 - v.getY()*h*2);
				int dxb2 = (int)(-u.getX()*w*0.75 - v.getX()*h*2);
				int dyb2 = (int)(-u.getY()*w*0.75 - v.getY()*h*2);
				int dx00 = (int)(-u.getX()*w);
				int dy00 = (int)(-u.getY()*w);
				
				
				p.moveRelativelyTo(x00,y00);
				p.lineRelativelyTo(dx01, dy01);
				p.lineRelativelyTo(dxm11,dym11);
				p.lineRelativelyTo(dxm12,dym12);
				p.lineRelativelyTo(dxm13,dym13);
				p.lineRelativelyTo(dxm14,dym14);
				p.lineRelativelyTo(dxm15,dym15);
				p.lineRelativelyTo(dxm21,dym21);
				p.lineRelativelyTo(dxm22,dym22);
				p.lineRelativelyTo(dxm23,dym23);
				p.lineRelativelyTo(dxm24,dym24);
				p.lineRelativelyTo(dxm25,dym25);
				p.lineRelativelyTo(dx11,dy11);
				p.lineRelativelyTo(dx10,dy10);
				p.curveRelativelyTo(dxb1,dyb1,dxb2,dyb2,dx00,dy00);
				p.close();
	}
}
