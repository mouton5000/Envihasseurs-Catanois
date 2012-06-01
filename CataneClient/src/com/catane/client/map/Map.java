package com.catane.client.map;

import gwt.g2d.client.graphics.KnownColor;
import gwt.g2d.client.graphics.Surface;
import gwt.g2d.client.graphics.shapes.Shape;
import gwt.g2d.client.math.Vector2;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;

import com.catane.client.Colors.PlayerColors;
import com.catane.client.requests.Connectable;
import com.catane.client.requests.Connector;
import com.catane.shared.Collections2;
import com.catane.shared.Math2;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.core.client.JsArrayInteger;


public class Map extends Surface implements Connectable {

	/**
	 * Nombres d'hexagones sur une ligne de la carte
	 */
	public static final int MAP_HW = 5;

	/**
	 * Nombres d'hexagones sur une colone de la carte
	 */
	public static final int MAP_HH = 6;

	/**
	 * Coordonnées actuelle du point supérieur gauche du canvas.
	 */
	Vector2 origin;


	private Map(int width, int height){
		super(width,height);
		origin = new Vector2(0,0);

		this.addClickHandler(new MapClickHandler(this));

		connectMap();
		draw();

	}
	private static Map littleMap;

	private static final int LITTLE_MAP_WIDTH = 800;
	private static final int LITTLE_MAP_HEIGHT = 500;

	public static Map getLittleMap(){
		if(littleMap == null)
			littleMap = new Map(LITTLE_MAP_WIDTH, LITTLE_MAP_HEIGHT);
		return littleMap;
	}

	private void drawHexagones(){
		for(int[] infos : getHexagones())
			this.drawHexagone(infos[0], map[infos[0]-1], infos[1], infos[2]);

	}

	public void drawPions(){
		for(int[] infos : getHexagones()){
			if(brigands.contains(infos[0])){
				this.drawBrigand(infos[0], infos[1], infos[2]);
			}
			if(pirates.contains(infos[0]))
				this.drawPirate(infos[0], infos[1], infos[2]);
			if(colonies.containsKey(infos[0])){
				for(int[] tab : colonies.get(infos[0])){
					this.drawColonie(tab[0], infos[1], infos[2], tab[1]);
				}
			}
			if(villes.containsKey(infos[0])){
				for(int[] tab : villes.get(infos[0]))
					this.drawVille(tab[0], infos[1], infos[2], tab[1]);
			}
			if(routes.containsKey(infos[0])){
				for(int[] tab : routes.get(infos[0]))
					this.drawRoute(tab[0], tab[1], infos[1], infos[2],tab[2]);
			}
			if(bateauTransports.containsKey(infos[0])){
				for(int[] tab : bateauTransports.get(infos[0]))
					this.drawBateauTransport(tab[0], tab[1], infos[1], infos[2], tab[2]);
			}
			if(cargos.containsKey(infos[0])){
				for(int[] tab : cargos.get(infos[0]))
					this.drawCargo(tab[0], tab[1], infos[1], infos[2], tab[2]);
			}
			if(voilliers.containsKey(infos[0])){
				for(int[] tab : voilliers.get(infos[0]))
					this.drawVoillier(tab[0], tab[1], infos[1], infos[2], tab[2]);
			}
		}
	}

	private void draw(){
		this.fillBackground(KnownColor.BLACK);

		drawHexagones();
		drawPions();
	}

	/**
	 * Renvoie la largeur actuelle des hexagones. Par largeur, on entends
	 * la valeur de CataneShapeBuild.HLARGEUR modifiée suite à un zoom de
	 * la carte.
	 * @return
	 */
	private double getHLargeur(){
		return CataneShapeBuilder.HLARGEUR;
	}

	/**
	 * Renvoie la largeur actuelle des hexagones. Par largeur, on entends
	 * la valeur de CataneShapeBuild.HLONGUEUR modifiée suite à un zoom de
	 * la carte.
	 * @return
	 */
	private double getHLongueur(){
		return CataneShapeBuilder.HLONGUEUR;
	}

	private final HexaType[] map= {
			HexaType.MER, HexaType.PORT, HexaType.MER, HexaType.MER, HexaType.MER, 
			HexaType.MER, HexaType.MER, HexaType.MER, HexaType.MER, HexaType.MER, 
			HexaType.MER, HexaType.BLE, HexaType.MER, HexaType.MER, HexaType.BOIS, 
			HexaType.BOIS, HexaType.CAILLOU, HexaType.MER, HexaType.BLE, HexaType.MER, 
			HexaType.MER, HexaType.DESERT, HexaType.MER, HexaType.MER, HexaType.OR, 
			HexaType.OR, HexaType.BLE, HexaType.MER, HexaType.MARCHE, HexaType.MER, 
			HexaType.MER, HexaType.MARCHE, HexaType.MER, HexaType.MER, HexaType.MOUTON, 
			HexaType.MARCHE, HexaType.MOUTON, HexaType.MER, HexaType.ARGILE, HexaType.MER, 
			HexaType.MER, HexaType.ARGILE, HexaType.MER, HexaType.MER, HexaType.PORT, 
			HexaType.MER, HexaType.BOIS, HexaType.MER, HexaType.MER, HexaType.MER, 
			HexaType.MER, HexaType.MER, HexaType.MER, HexaType.MER, HexaType.MER, 
			HexaType.MER, HexaType.PORT, HexaType.MER, HexaType.MER, HexaType.MER};

	/**
	 * Renvoie les hexagones actuellement visibles sur la carte associé à deux chiffres :
	 * s'ils sont nuls, c'est qu'on observe la carte au centre du canvas, sinon c'est qu'on
	 * observe une copie de la carte du fait que celle ci est un tore. Si le premier chiffre
	 * est négatif, on est "au dessus" de la carte originale, positif, en dessous. Le second
	 * concerne la gauche et la droite.
	 * @return
	 */
	private ArrayList<int[]> getHexagones(){
		int[] limits = getLimits();
		ArrayList<int[]> ar = new ArrayList<int[]>();
		int[] infos;
		int mline, mcolumn, dcol;
		for(int column = limits[2]; column <= limits[3]; column ++){
			dcol = Math2.mod(column,2);
			for(int line = limits[0]; line <= limits[1]; line ++){
				if(Math2.mod(line,2) == dcol){
					infos = new int[3];

					mline = Math2.mod(line,2*MAP_HH);
					mcolumn = Math2.mod(column,2*MAP_HW);

					infos[0] = mline * MAP_HW + mcolumn/2+1;
					infos[1] = Math2.div(line,2*MAP_HH);
					infos[2] = Math2.div(column,2*MAP_HW);
					ar.add(infos);
				}
			}
		}
		return ar;
	}

	/**
	 * Renvoie les lignes et colonnes limites contenue actuellement dans la carte.
	 * @return
	 */
	private int[] getLimits(){
		double x0 = origin.getX(),
				x1 = x0 + this.getWidth(),
				y0 = origin.getY(),
				y1 = y0 + this.getHeight();
		int line0 = getLine(y0, true);
		int line1 = getLine(y1, false);
		int column0 = getColumn(x0, true);
		int column1 = getColumn(x1, false);

		int[] limits = {line0, line1, column0, column1};
		return limits;
	}

	/**
	 * Renvoie la colonne la plus à gauche (resp droite) contenant l'abscisse si left est vrai (resp faux)
	 * @param x
	 * @param left
	 * @return
	 */
	private int getColumn(double x, boolean left) {
		return 
				Math2.div((int)(x-(left?-1:-2)*getHLargeur()),
						(int)(getHLargeur()*3));

	}

	/**
	 * Renvoie la ligne la plus haute (resp basse) contenant l'ordonnée y si top est vrai (resp faux).
	 * @param y
	 * @param top
	 * @return
	 */
	private int getLine(double y, boolean top) {
		int line = Math2.div((int)y,(int)getHLongueur());
		return top?line:line+1;

	}

	/**
	 * Renvoie l'hexagone actuellement affiché sur la cartes aux coordonnées M : (x,y).
	 * @param x
	 * @param y
	 * @return
	 */
	int getHexagoneFromCoords(double x, double y){
		double x0 = origin.getX(),
				x1 = Math2.mod((int)(x0 + x), (int)(MAP_HW*6*getHLargeur())),
				y0 = origin.getY(),
				y1 = Math2.mod((int)(y0 + y), (int)(MAP_HH*2*getHLongueur()));

		double l = getHLargeur();
		double h = getHLongueur();

		double mc = Math2.mod((int)x1, (int)(6*l));
		int column = Math2.div((int)x1, (int)(6*l));
		if(x1 >= MAP_HW*6*l - 2*l)
			column -= MAP_HW;
		int ml = Math2.mod((int)y1, (int)(2*h));
		int line = Math2.div((int)y1, (int)(2*h));
		if(y1 >= MAP_HH*2*h - h)
			line -= MAP_HH;

		int hex;
		if(mc >= 5*l || mc < l)
		{
			if(ml >= h)
				line++;
			if(mc>=5*l)
				column++;
			hex = 2*line*MAP_HW+column;
		}
		else if(mc >= 2*l && mc < 4*l)
		{
			hex =  2*line*MAP_HW+column+MAP_HW;
		}

		else{ 
			double alpha = -1;
			boolean b = false;
			if(mc >= l  && mc < 2*l){
				alpha = mc-l;
			}
			else if(b = (mc >= 4*l  && mc < 5*l)){
				alpha = 5*l-mc;
			}
			if(ml < (l-alpha)*h/l || ml > 2*h-(l-alpha)*h/l){
				if (b) column++;
				if(ml >= h)
					line++;
				hex =  2*line*MAP_HW+column;
			}
			else{
				if(x1 >= MAP_HW*6*l - 2*l && x1 < MAP_HW*6*l - l)
					column += MAP_HW;
				hex =  2*line*MAP_HW+column + MAP_HW;
			}
		}
		return Math2.mod(hex, 2*MAP_HW*MAP_HH) + 1;
	}

	int getIntersectionFromCoords(double x, double y){
		int i = getHexagoneFromCoords(x, y);
		System.out.print(i+" ");
		Vector2 c = getHexagoneCoords(i, 0, 0);
		double x0 = origin.getX(),
				x1 = Math2.mod((int)(x0 + x), (int)(MAP_HW*6*getHLargeur())),
				y0 = origin.getY(),
				y1 = Math2.mod((int)(y0 + y), (int)(MAP_HH*2*getHLongueur()));

		double l = getHLargeur();
		double h = getHLongueur();

		x1 -= c.getX();
		y1 -= c.getY();

		int iq = (i-1)/MAP_HW;
		boolean plan1 = (iq%2 == 0);
		int[] inters = new int[6]; 
		if(plan1){

			if(x1 >= MAP_HW*6*l - 2*l)
				x1 -= MAP_HW*6*l;
			if(y1 >= MAP_HH*2*h - h)
				y1 -= MAP_HH*2*h;

			inters[0] = 2*i-2;
			inters[1] = 2*i-1;
			inters[2] = 2*i+2*MAP_HW-1;
			inters[3] = 2*i+4*MAP_HW-1;
			inters[4] = 2*i+4*MAP_HW-2;
			inters[5] = 2*i+2*MAP_HW-2;
		}
		else
		{
			inters[0] = 2*i-1;
			inters[1] = inters[0]+(((inters[0]+1)%(2*MAP_HW)==0)?-9:1);
			inters[2] = inters[1]+MAP_HW*2;
			inters[3] = inters[1]+MAP_HW*4;
			inters[5] = inters[0]+2*MAP_HW;
			inters[4] = inters[0]+4*MAP_HW;
		}

		double[][] delta = {{-l,-h},{l,-h},{2*l,0},{l,h},{-l,h},{-2*l,0}};
		int inter = 0;
		double dist = Double.MAX_VALUE,d;
		for(int j = 0; j<6;j++){
			d = Math2.dist(x1,y1,delta[j][0], delta[j][1]);
			if(dist > d){
				dist = d;
				inter = inters[j];
			}
		}
		return Math2.mod(inter,4*MAP_HW*MAP_HH)+1;
	}

	int[] getArreteFromCoords(double x, double y){
		int i = getHexagoneFromCoords(x, y);
		System.out.print(i+" ");
		Vector2 c = getHexagoneCoords(i, 0, 0);
		double x0 = origin.getX(),
				x1 = Math2.mod((int)(x0 + x), (int)(MAP_HW*6*getHLargeur())),
				y0 = origin.getY(),
				y1 = Math2.mod((int)(y0 + y), (int)(MAP_HH*2*getHLongueur()));

		double l = getHLargeur();
		double h = getHLongueur();

		x1 -= c.getX();
		y1 -= c.getY();

		int iq = (i-1)/MAP_HW;
		boolean plan1 = (iq%2 == 0);
		int[] inters = new int[6]; 
		if(plan1){

			if(x1 >= MAP_HW*6*l - 2*l)
				x1 -= MAP_HW*6*l;
			if(y1 >= MAP_HH*2*h - h)
				y1 -= MAP_HH*2*h;

			inters[0] = 2*i-2;
			inters[1] = 2*i-1;
			inters[2] = 2*i+2*MAP_HW-1;
			inters[3] = 2*i+4*MAP_HW-1;
			inters[4] = 2*i+4*MAP_HW-2;
			inters[5] = 2*i+2*MAP_HW-2;
		}
		else
		{
			inters[0] = 2*i-1;
			inters[1] = inters[0]+(((inters[0]+1)%(2*MAP_HW)==0)?-9:1);
			inters[2] = inters[1]+MAP_HW*2;
			inters[3] = inters[1]+MAP_HW*4;
			inters[5] = inters[0]+2*MAP_HW;
			inters[4] = inters[0]+4*MAP_HW;
		}

		double[][] delta = {{0,-h},{3*l/2,-h/2},{3*l/2,h/2},{0,h},{-3*l/2,h/2},{-3*l/2,-h/2}};
		int mj = 0;
		double dist = Math2.dist(x1,y1,delta[0][0], delta[0][1]),d;
		for(int j = 1; j<6;j++){
			d = Math2.dist(x1,y1,delta[j][0], delta[j][1]);
			if(dist > d){
				dist = d;
				mj = j;
			}
		}

		int[] arrete = new int[2];
		switch(mj){
		case 0: 
			arrete[0] = inters[0];
			arrete[1] = inters[1];
			break;
		case 1: 
			arrete[0] = inters[1];
			arrete[1] = inters[2];
			break;
		case 2: 
			arrete[0] = inters[2];
			arrete[1] = inters[3];
			break;
		case 3: 
			arrete[0] = inters[3];
			arrete[1] = inters[4];
			break;
		case 4: 
			arrete[0] = inters[4];
			arrete[1] = inters[5];
			break;
		case 5: 
			arrete[0] = inters[5];
			arrete[1] = inters[0];
			break;

		};
		arrete[0] = Math2.mod(arrete[0],4*MAP_HW*MAP_HH)+1;
		arrete[1] = Math2.mod(arrete[1],4*MAP_HW*MAP_HH)+1;
		return arrete;
	}

	/**
	 * Renvoie les coordonnées centrale de l'hexagone numéro i.
	 * le premier hexagone est 1. (bouuuhh)
	 * @param i
	 * @return
	 */
	private Vector2 getHexagoneCoords(int i, int deltaLine, int deltaColumn){
		i--;

		Vector2 v = new Vector2();
		/*
		 * Il existe deux types de lignes et deux types de colones d'hexagones
		 * quand on les numérotes dans l'ordre horizontal (et non pas suivant un
		 * plan 2D d'angle 60°). Ces lignes et colonnes forment deux plans superposés
		 * et décalés d'un déplacement d'hexagone par un côté oblique.
		 * 
		 * column désigne la colonne et line la ligne dans le plan où se trouve l'hexagone. 
		 * 
		 */
		int iq = i/MAP_HW, column = i%MAP_HW, line = iq/2;

		/* Si line1 est vrai, alors en numérotant les lignes de la carte en commençant par
		 * 0, cet hexagone est sur une ligne paire. Il est dans le premier plan. Sinon il
		 * dans le second.  
		 */

		boolean plan1 = (iq%2 == 0);
		double x0, y0;

		double l = getHLargeur();
		double h = getHLongueur();

		if(plan1){
			x0 = 0;
			y0 = 0;
		}
		else
		{
			x0 = l*3.0;
			y0 = h;
		}

		v.setX(x0 + column * l*6 + deltaColumn * 6*l * MAP_HW);
		v.setY(y0 + line * h*2 + deltaLine * 2*h * MAP_HH);

		return v;
	}

	/**
	 * Dessine un hexagone numéro i
	 * @param i-
	 * @param j
	 * @return
	 */
	public Map drawHexagone(int i, HexaType type, int deltaLine, int deltaColumn){
		Vector2 v = getHexagoneCoords(i, deltaLine, deltaColumn);

		Shape s = new CataneShapeBuilder()
		.drawHexagone(v.getX(), v.getY()).build();
		this.setFillStyle(type.getColor());
		this.fillShape(s);
		this.setStrokeStyle(KnownColor.BLACK);
		this.strokeShape(s);
		return this;
	}

	/**
	 * Dessine un brigand sur l'hexagone numéro i
	 * @param i
	 * @param j
	 * @return
	 */
	public Map drawBrigand(int i, int deltaLine, int deltaColumn){
		Vector2 v = getHexagoneCoords(i,deltaLine, deltaColumn);


		this.setFillStyle(KnownColor.BLACK);
		this.fillShape(new CataneShapeBuilder()
		.drawBrigand(v.getX(), v.getY()).build());
		return this;
	}

	/**
	 * Dessine un pirate sur l'hexagone numéro i
	 * @param i
	 * @param j
	 * @return
	 */
	public Map drawPirate(int i, int deltaLine, int deltaColumn){
		Vector2 v = getHexagoneCoords(i,deltaLine, deltaColumn);

		this.setFillStyle(KnownColor.BLACK);
		this.fillShape(new CataneShapeBuilder()
		.drawPirate(v.getX(), v.getY()).build());
		return this;
	}

	/**
	 * Renvoie l'hexagone situé "en dessous" de l'intersection numéro i
	 * @param i
	 * @return
	 */
	private static int getHexagoneFromIntersection(int i){

		i--;
		int iq = i/(2*MAP_HW), column = i%(2*MAP_HW);
		boolean plan1 = (iq%2 == 0);
		if(plan1)
			return i/2+1; 
		else
		{
			if(column == 0)
				i+=2*MAP_HW;
			return i/2+1;
		}
	}
	/**
	 * Renvoie les coordonnées de l'intersection numéro i.
	 * @param i
	 * @return
	 */
	private Vector2 getIntersectionCoord(int i, int deltaLine, int deltaColumn){
		i--;

		Vector2 v = new Vector2();
		int iq = i/(2*MAP_HW), column = i%(2*MAP_HW), line = iq/2;
		boolean plan1 = (iq%2 == 0);

		double x0, y0;
		double l = getHLargeur();
		double h = getHLongueur();
		if(plan1){
			if(i%2 == 0){
				x0 = -l;
				y0 = -h;
			}
			else
			{
				x0 = l;
				y0 = -h;
			}
		}
		else
		{
			if(i%2 == 0){
				x0 = -l*2.0;
				y0 = 0;
			}
			else
			{
				x0 = l*2.0;
				y0 = 0;
			}
		}

		v.setX(x0  + column/2 * l*6.0 + deltaColumn * 6*l * MAP_HW);
		v.setY(y0  + line * h*2.0 + deltaLine * 2*h * MAP_HH);

		return v;
	}

	/**
	 * Dessine une colonie sur l'intersection numéro i
	 * @param i
	 * @param j
	 * @param left
	 * @return
	 */
	public Map drawColonie(int i, int deltaLine, int deltaColumn, int player){
		return drawBatiment(i,true, deltaLine, deltaColumn, player);
	}

	/**
	 * Dessinge une ville sur l'intersection numéro i
	 * @param i
	 * @param j
	 * @param left
	 * @return
	 */
	public Map drawVille(int i, int deltaLine, int deltaColumn, int player){
		return drawBatiment(i,false, deltaLine, deltaColumn, player);
	}

	private Map drawBatiment(int i, boolean isColonie, int deltaLine, int deltaColumn, int player){
		this.setFillStyle(PlayerColors.getPlayerColor(player));
		Vector2 v = getIntersectionCoord(i, deltaLine, deltaColumn);
		Shape s;
		if(isColonie)
			s = new CataneShapeBuilder()
		.drawColonie(v.getX(), v.getY()).build();
		else
			s = new CataneShapeBuilder()
		.drawVille(v.getX(), v.getY()).build();

		this.fillShape(s);
		this.setStrokeStyle(KnownColor.BLACK);
		this.strokeShape(s);

		return this;
	}

	/**
	 * Dessinge une route sur l'arrête d'intersections i et j, 
	 * sur le coté haut gauche si position < 0, haut si position = 0
	 * haut droit si position > 0.
	 * @param i
	 * @param j
	 * @param left
	 * @return
	 */
	public Map drawRoute(int i, int j, int deltaLine, int deltaColumn, int player){
		return drawLink(i,j,LinkType.ROUTE, deltaLine, deltaColumn, player);
	}

	/**
	 * Dessinge un bateau de transport sur l'arrête d'intersections i et j, 
	 * sur le coté haut gauche si position < 0, haut si position = 0
	 * haut droit si position > 0.
	 * @param i
	 * @param j
	 * @param left
	 * @return
	 */
	public Map drawBateauTransport(int i, int j, int deltaLine, int deltaColumn, int player){
		return drawLink(i,j,LinkType.TRANSPORT,deltaLine, deltaColumn, player);
	}

	/**
	 * Dessinge un bateau cargo sur l'arrête d'intersections i et j, 
	 * sur le coté haut gauche si position < 0, haut si position = 0
	 * haut droit si position > 0.
	 * @param i
	 * @param j
	 * @param left
	 * @return
	 */
	public Map drawCargo(int i, int j, int deltaLine, int deltaColumn, int player){
		return drawLink(i,j,LinkType.CARGO, deltaLine, deltaColumn, player);
	}

	/**
	 * Dessinge un bateau voillier sur l'arrête d'intersections i et j, 
	 * sur le coté haut gauche si position < 0, haut si position = 0
	 * haut droit si position > 0.
	 * @param i
	 * @param j
	 * @param left
	 * @return
	 */
	public Map drawVoillier(int i, int j, int deltaLine, int deltaColumn, int player){
		return drawLink(i,j,LinkType.VOILLIER, deltaLine, deltaColumn, player);
	}


	private enum LinkType {ROUTE, TRANSPORT, CARGO, VOILLIER};

	public Map drawLink(int i, int j, LinkType link, int deltaLine, int deltaColumn, int player){
		this.setFillStyle(PlayerColors.getPlayerColor(player));
		Vector2 v1 = getIntersectionCoord(i,deltaLine, deltaColumn),
				v2 = getIntersectionCoord(j, deltaLine, deltaColumn);
		double x1 = v1.getX(), y1 = v1.getY(), x2 = v2.getX(), y2 = v2.getY();
		Shape s;
		switch(link){
		case ROUTE:
			s = new CataneShapeBuilder()
			.drawRoute(x1,y1,x2,y2).build();
			break;
		case TRANSPORT:
			s = new CataneShapeBuilder()
			.drawBateauTransport(x1,y1,x2,y2).build();
			break;
		case CARGO:
			s = new CataneShapeBuilder()
			.drawCargo(x1,y1,x2,y2).build();
			break;
		case VOILLIER:
			s = new CataneShapeBuilder()
			.drawVoillier(x1,y1,x2,y2).build();
			break;
		default : s = null;
		}

		this.fillShape(s);
		this.setStrokeStyle(KnownColor.BLACK);
		this.strokeShape(s);
		return this;
	}

	public Map translateX(double x){
		double x0 = origin.getX(),
				limitColumn = 6*getHLargeur() * MAP_HW;

		if(x0-x < -limitColumn)
			x-=limitColumn;
		else if (x0-x > limitColumn)
			x+=limitColumn;

		origin.setX(origin.getX()-x);

		super.translate(x,0);
		return this;
	}

	public Map translateY(double y){

		double y0 = origin.getY(),
				limitLine = 2*getHLongueur() * MAP_HH;

		if(y0-y < -limitLine)
			y-=limitLine;
		else if (y0-y > limitLine)
			y+=limitLine;

		origin.setY(origin.getY()-y);

		super.translate(0,y);
		return this;
	}

	public void left() {
		this.translateX(100);
		this.draw();
	}

	public void right() {
		this.translateX(-100);
		this.draw();
	}

	public void up() {
		this.translateY(100);

		this.draw();
	}

	public void down() {
		this.translateY(-100);
		this.draw();
	}


	/**
	 * Informations concernant les colonies : 
	 * hashMap des hexagones vers les intersections et joueurs propriétaire
	 */
	private HashMap<Integer, ArrayList<int[]>> colonies = new HashMap<Integer,ArrayList<int[]>>();

	/**
	 * Informations concernant les villes : 
	 * hashMap des hexagones vers les intersections et le joueurs propriétaire
	 */
	private HashMap<Integer, ArrayList<int[]>> villes = new HashMap<Integer,ArrayList<int[]>>();

	/**
	 * Informations concernant les routes : 
	 * HashMap des hexagones vers un tableaux de 3 entiers, les intersections de l'arrete et le joueur.
	 */
	private HashMap<Integer,ArrayList<int[]>> routes = new HashMap<Integer,ArrayList<int[]>>();

	/**
	 * Informations concernant les bateaux : 
	 * HashMap des hexagones vers un tableaux de 3 entiers, les intersections de l'arrete et le joueur.
	 */
	private HashMap<Integer,ArrayList<int[]>> bateauTransports = new HashMap<Integer,ArrayList<int[]>>();

	/**
	 * Informations concernant les cargos : 
	 * HashMap des hexagones vers un tableaux de 3 entiers, les intersections de l'arrete et le joueur.
	 */
	private HashMap<Integer, ArrayList<int[]>> cargos = new HashMap<Integer,ArrayList<int[]>>();

	/**
	 * Informations concernant les voilliers : 
	 * HashMap des hexagones vesr tableaux de 3 entiers, les intersections de l'arrete et le joueur.
	 */
	private HashMap<Integer, ArrayList<int[]>> voilliers = new HashMap<Integer,ArrayList<int[]>>();

	/**
	 * Informations concernant les brigands : 
	 * les divers hexagones contenant un brigand.
	 */
	private HashSet<Integer> brigands = new HashSet<Integer>();

	/**
	 * Informations concernant les pirates : 
	 * les divers hexagones contenant un pirate.
	 */
	private HashSet<Integer> pirates = new HashSet<Integer>();

	/**
	 * Se connecte au serveur pour chercher toutes les informations nécessaires à la
	 * complétion de la carte
	 */
	private void connectMap(){
		new Connector("map/infos/3/0", this);
	}

	@Override
	public void callback(JavaScriptObject json) {
		if (json == null)
			displayError();
		else{
			MapInfos jmap = asMap(json);
			JsArrayInteger brs = jmap.getBrigands();
			brigands.clear();
			for(int i = 0; i<brs.length(); i++)
				brigands.add(brs.get(i));

			JsArrayInteger prs = jmap.getPirates();
			pirates.clear();
			for(int i = 0; i<prs.length(); i++)
				pirates.add(prs.get(i));

			int[] tab;

			JsArray<BatimentInfos> cols = jmap.getColonies();
			colonies.clear();
			BatimentInfos col;
			for(int i = 0; i<cols.length(); i++){
				col = cols.get(i);
				tab = new int[2]; tab[0] = col.getPosition(); tab[1] = col.getJoueur();
				Collections2.put(colonies, getHexagoneFromIntersection(tab[0]), tab);
			}

			JsArray<BatimentInfos> vils = jmap.getVilles();
			villes.clear();
			BatimentInfos vil;
			for(int i = 0; i<vils.length(); i++){
				vil = vils.get(i);
				tab = new int[2]; tab[0] = vil.getPosition(); tab[1] = vil.getJoueur();
				Collections2.put(villes, getHexagoneFromIntersection(tab[0]), tab);
			}

			JsArray<LienInfos> routs = jmap.getRoutes();
			routes.clear();
			LienInfos rout;
			for(int i = 0; i<routs.length(); i++){
				rout = routs.get(i);
				tab = new int[3]; 
				tab[0] = rout.getPosition1(); 
				tab[1] = rout.getPosition2(); 
				tab[2] = rout.getJoueur();
				Collections2.put(routes, getHexagoneFromIntersection(tab[0]), tab);
			}

			JsArray<LienInfos> transp = jmap.getBateauxTransports();
			bateauTransports.clear();
			LienInfos trans;
			for(int i = 0; i<transp.length(); i++){
				trans = transp.get(i);
				tab = new int[3]; 
				tab[0] = trans.getPosition1(); 
				tab[1] = trans.getPosition2(); 
				tab[2] = trans.getJoueur();
				Collections2.put(bateauTransports, getHexagoneFromIntersection(tab[0]), tab);
			}

			JsArray<LienInfos> cargs = jmap.getCargos();
			cargos.clear();
			LienInfos carg;
			for(int i = 0; i<cargs.length(); i++){
				carg = cargs.get(i);
				tab = new int[3]; 
				tab[0] = carg.getPosition1(); 
				tab[1] = carg.getPosition2(); 
				tab[2] = carg.getJoueur();
				Collections2.put(cargos, getHexagoneFromIntersection(tab[0]), tab);
			}

			JsArray<LienInfos> voils = jmap.getVoilliers();
			voilliers.clear();
			LienInfos voil;
			for(int i = 0; i<voils.length(); i++){
				voil = voils.get(i);
				tab = new int[3]; 
				tab[0] = voil.getPosition1(); 
				tab[1] = voil.getPosition2(); 
				tab[2] = voil.getJoueur();
				Collections2.put(voilliers, getHexagoneFromIntersection(tab[0]), tab);
			}


			draw();
		}
	}

	/**
	 * Cast JavaScriptObject as JsArray of StockData.
	 */
	private final native MapInfos asMap(JavaScriptObject jso) /*-{
	    return jso;
	  }-*/;

	@Override
	public void displayError() {
		// TODO Auto-generated method stub

	}

}

