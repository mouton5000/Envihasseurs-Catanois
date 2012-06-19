package com.catane.client.map;

import java.util.ArrayList;
import java.util.HashSet;

import org.vaadin.gwtgraphics.client.DrawingArea;
import org.vaadin.gwtgraphics.client.VectorObject;

import com.catane.client.User;
import com.catane.client.requests.Connectable;
import com.catane.client.requests.Connector;
import com.catane.shared.Math2;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.core.client.JsArrayInteger;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;

public class Map extends DrawingArea implements Connectable {


	/**
	 * Nombres d'hexagones sur une ligne de la carte
	 */
	public static final int MAP_HW = 5;

	/**
	 * Nombres d'hexagones sur une colone de la carte
	 */
	public static final int MAP_HH = 6;


	private MapMouseHandler mmh;
	private MapClickHandler mch; 

	public Map(int width, int height) {
		super(width,height);

		mmh = new MapMouseHandler(this);
		this.addMouseMoveHandler(mmh);
		this.addMouseOutHandler(mmh);

		buildPlateau();
		connectMap();
	}
	
	public void setMapClickHandler(MapClickHandler mch){
		this.mch = mch;
	}


	private static Map littleMap;

	public static final int LITTLE_MAP_WIDTH = 800;
	public static final int LITTLE_MAP_HEIGHT = 500;

	public static Map getLittleMap(){
		if(littleMap == null)
			littleMap = new Map(LITTLE_MAP_WIDTH, LITTLE_MAP_HEIGHT);
		return littleMap;
	}

	private static Map bigMap;

	private static final int BIG_MAP_WIDTH = 1400;
	private static final int BIG_MAP_HEIGHT = 800;

	public static Map getBigMap() {
		if(bigMap == null)
			bigMap = new Map(BIG_MAP_WIDTH, BIG_MAP_HEIGHT);
		return bigMap;
	}

	ArrayList<HexagoneInfos> plateau = new ArrayList<HexagoneInfos>();
	private void buildPlateau() {
		HexagoneInfos hi;
		for(int i = 1; i<=2*MAP_HW*MAP_HH;i++){
			hi = new HexagoneInfos(i,Terre.getTerre(terresRepartition[i-1]));
			plateau.add(hi);
			hi.setColor(colorMap[i-1].getColor());
		}

		int i,il,ir,iu,id,iul,iur,idl,idr;
		boolean plan1 = true;
		for(int line = 0; line<2*MAP_HH;line++){
			for(int column = 0; column <MAP_HW; column++){
				i = line*MAP_HW+column;
				hi = plateau.get(i);

				il = line*MAP_HW+Math2.mod(column-1,MAP_HW);
				ir = line*MAP_HW+Math2.mod(column+1,MAP_HW);
				iu = Math2.mod((line-2)*MAP_HW+column,2*MAP_HW*MAP_HH);
				id = Math2.mod((line+2)*MAP_HW+column,2*MAP_HW*MAP_HH);

				if(plan1){
					iul = Math2.mod((line-1)*MAP_HW+Math2.mod(column-1,MAP_HW),2*MAP_HW*MAP_HH);
					iur = Math2.mod((line-1)*MAP_HW+column,2*MAP_HW*MAP_HH);
					idl = Math2.mod((line+1)*MAP_HW+Math2.mod(column-1,MAP_HW),2*MAP_HW*MAP_HH);
					idr = Math2.mod((line+1)*MAP_HW+column,2*MAP_HW*MAP_HH);
				}
				else
				{
					iul = Math2.mod((line-1)*MAP_HW+column,2*MAP_HW*MAP_HH);
					iur = Math2.mod((line-1)*MAP_HW+Math2.mod(column+1,MAP_HW),2*MAP_HW*MAP_HH);
					idl = Math2.mod((line+1)*MAP_HW+column,2*MAP_HW*MAP_HH);
					idr = Math2.mod((line+1)*MAP_HW+Math2.mod(column+1,MAP_HW),2*MAP_HW*MAP_HH);

				}
				hi.setLeft(plateau.get(il));
				hi.setRight(plateau.get(ir));
				hi.setUp(plateau.get(iu));
				hi.setDown(plateau.get(id));
				hi.setUpLeft(plateau.get(iul));
				hi.setUpRight(plateau.get(iur));
				hi.setDownLeft(plateau.get(idl));
				hi.setDownRight(plateau.get(idr));
			}
			plan1 = !plan1;
		}

		drawFirst();

	}

	private void drawFirst(){
		for(int i = 1; i<=2*MAP_HW*MAP_HH;i++){
			drawHexagone(i);
		}
	}

	public void center(){
		Terre t = Terre.getChosenOne();
		int hindex = centers[t.getIndex()];
		center(plateau.get(hindex));
	}
	
	private void center(HexagoneInfos hi){
		// TODO
	}
	
	public void draw(){
		Terre t = Terre.getChosenOne();
		HexagonePath hex;
		HexagoneInfos hi;
		for(int i = 0; i<map.size();i++){
			hex = map.get(i);
			hi = hex.getInfos();
			hex.setFillColor(hi.getColor());
			double opacity = (hi.getTerre() == t)?1:0.5;
			hex.setFillOpacity(opacity);
			int[] coords = hex.getCoords();
			PionPath p;
			
			if((p = hi.getVoleur()) != null){
				p.setX(coords[0]);
				p.setY(coords[1]);
				p.setFillOpacity(opacity);
				if(p.getParent() == null)
					this.add(p);
			}
			if((p = hi.getIntLeft()) != null){
				p.setX(coords[0]-getHLargeur());
				p.setY(coords[1]-getHLongueur());
				p.setFillOpacity(opacity);
				if(p.getParent() == null)
					this.add(p);
			}

			if((p = hi.getIntRight()) != null){
				p.setX(coords[0]+getHLargeur());
				p.setY(coords[1]-getHLongueur());
				p.setFillOpacity(opacity);
				if(p.getParent() == null)
					this.add(p);
			}

			VectorObject vo;
			if((vo = hi.getArLeft()) != null){
				int x = coords[0]-getHLargeur()*3/2;
				int y = coords[1]-getHLongueur()/2;
				
				if(vo instanceof PionPath){
					((PionPath)vo).setX(x);
					((PionPath)vo).setY(y);
					((PionPath) vo).setFillOpacity(opacity);
				}
				else
				{
					((PionsJoueursGroup)vo).setX(x);
					((PionsJoueursGroup)vo).setY(y);
					((PionsJoueursGroup)vo).setFillOpacity(opacity);
				}
				if(vo.getParent() == null)
					this.add(vo);
			}

			if((vo = hi.getArUp()) != null){
				int x = coords[0];
				int y = coords[1]-getHLongueur();
				if(vo instanceof PionPath){
					((PionPath)vo).setX(x);
					((PionPath)vo).setY(y);
					((PionPath) vo).setFillOpacity(opacity);
				}
				else
				{
					((PionsJoueursGroup)vo).setX(x);
					((PionsJoueursGroup)vo).setY(y);
					((PionsJoueursGroup)vo).setFillOpacity(opacity);
				}
				if(vo.getParent() == null)
					this.add(vo);
			}

			if((vo = hi.getArRight()) != null){
				int x = coords[0]+getHLargeur()*3/2;
				int y = coords[1]-getHLongueur()/2;
				if(vo instanceof PionPath){
					((PionPath)vo).setX(x);
					((PionPath)vo).setY(y);
					((PionPath) vo).setFillOpacity(opacity);
				}
				else
				{
					((PionsJoueursGroup)vo).setX(x);
					((PionsJoueursGroup)vo).setY(y);
					((PionsJoueursGroup)vo).setFillOpacity(opacity);
				}
				if(vo.getParent() == null)
					this.add(vo);
			}

		}
	}

	static final HexaType[] colorMap= {
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

	static final int[] terresRepartition = {
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1,
		0,0,0,1,1};

	static final String[] terres = {
		"Terre gauche",
		"Terre droite"
	};
	
	static final int[] centers = {
		26,28
	};
	
	
	/**
	 * Renvoie les coordonnées centrale de l'hexagone numéro i.
	 * le premier hexagone est 1. (bouuuhh)
	 * @param i
	 * @return
	 */
	private int[] getHexagoneCoords(int i){
		i--;

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
		int x0, y0;

		int l = getHLargeur();
		int h = getHLongueur();

		if(plan1){
			x0 = 0;
			y0 = 0;
		}
		else
		{
			x0 = l*3;
			y0 = h;
		}

		int[] v = {x0 + column * l*6,
				y0 + line * 2*h};

		return v;
	}

	/**
	 * Renvoie un tableau contenant le numéro de l'hexagone situé "en dessous" de l'intersection numéro i
	 * et 0 si l'intersection est à gauche, ou 1 sinon 
	 * @param i
	 * @return 
	 */
	private static int[] getHexagoneFromIntersection(int i){

		i--;
		int iq = i/(2*MAP_HW), column = i%(2*MAP_HW);
		int[] ar = new int[2];
		boolean plan1 = (iq%2 == 0);
		if(plan1){
			ar[0] = i/2+1;
			ar[1] = (i%2 == 0)?0:1; 
		}
		else
		{
			if(column == 0)
				i+=2*MAP_HW;
			ar[0] = (i+1)/2;
			ar[1] = (i%2 == 1)?0:1;
		}
		return ar;
	}

	ArrayList<HexagonePath> map = new ArrayList<HexagonePath>();

	/**
	 * Renvoie la largeur actuelle des hexagones. Par largeur, on entends
	 * la valeur de CataneShapeBuild.HLARGEUR modifiée suite à un zoom de
	 * la carte.
	 * @return
	 */
	private int getHLargeur(){
		return HexagonePath.HLARGEUR;
	}

	/**
	 * Renvoie la largeur actuelle des hexagones. Par largeur, on entends
	 * la valeur de CataneShapeBuild.HLONGUEUR modifiée suite à un zoom de
	 * la carte.
	 * @return
	 */
	private int getHLongueur(){
		return HexagonePath.HLONGUEUR;
	}

	/**
	 * Dessine un hexagone numéro i
	 * @param i-
	 * @param j
	 * @return
	 */
	public Map drawHexagone(final int i){
		int[] v = getHexagoneCoords(i);

		boolean bx = v[0] >= -2*getHLargeur()-10 && v[0] <= getWidth()+2*getHLargeur()+10;
		boolean by = v[1] >= -getHLongueur()-10 && v[1] <=  getHeight()+getHLongueur()+10;
		if(bx && by){
			final HexagonePath hexagone = new HexagonePath(v[0], v[1]);
			hexagone.setFillColor(colorMap[i-1].getColor());
			this.add(hexagone);
			hexagone.setInfos(plateau.get(i-1));
			map.add(hexagone);
			hexagone.addClickHandler(new ClickHandler() {
				
				@Override
				public void onClick(ClickEvent event) {
					Map.this.mch.onHexagoneClick(event);
				}
			});
		}
		return this;
	}



	private enum Direction{
		LEFT,RIGHT,UP,DOWN,UPLEFT,UPRIGHT,DOWNLEFT,DOWNRIGHT;
	}

	private void translate(Direction dir){
		boolean iterationFromTop;
		switch(dir){
		case DOWN:
			iterationFromTop = true;
			break;
		case DOWNLEFT:
			iterationFromTop = true;
			break;
		case DOWNRIGHT:
			iterationFromTop = true;
			break;
		case LEFT:
			iterationFromTop = false;
			break;
		case RIGHT:
			iterationFromTop = true;
			break;
		case UP:
			iterationFromTop = false;
			break;
		case UPLEFT:
			iterationFromTop = false;
			break;
		case UPRIGHT:
			iterationFromTop = false;
			break;
		default:
			return;
		}

		HexagonePath hex;
		if(iterationFromTop){
			for(int i = 0 ; i<map.size(); i++){
				hex = map.get(i);
				vanish(hex.getInfos());
				switch(dir){
				case RIGHT:
					hex.setInfos(hex.getInfos().getRight());
					break;
				case DOWN:
					hex.setInfos(hex.getInfos().getDown());
					break;
				case DOWNLEFT:
					hex.setInfos(hex.getInfos().getDownLeft());
					break;
				case DOWNRIGHT:
					hex.setInfos(hex.getInfos().getDownRight());
					break;
				}
			}
		}
		else
		{
			for(int i = map.size()-1 ; i>=0; i--){
				hex = map.get(i);
				vanish(hex.getInfos());
				switch(dir){
				case LEFT:
					hex.setInfos(hex.getInfos().getLeft());
					break;
				case UP:
					hex.setInfos(hex.getInfos().getUp());
					break;
				case UPLEFT:
					hex.setInfos(hex.getInfos().getUpLeft());
					break;
				case UPRIGHT:
					hex.setInfos(hex.getInfos().getUpRight());
					break;
				}
			}
		}
		draw();
	}

	private void vanish(HexagoneInfos infos) {
		VectorObject p;

		p = infos.getVoleur();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getIntLeft();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getIntRight();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getArLeft();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getArUp();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getArRight();
		if(p != null && p.getParent() == this)
			this.remove(p);
	}

	private Arrow left;
	private Arrow right;
	private Arrow up;
	private Arrow down;

	private Arrow upLeft;
	private Arrow upRight;
	private Arrow downLeft;
	private Arrow downRight;

	private Arrow currentArrow;

	private Map arrow(Arrow arrow){
		removeCurrentArrow();
		currentArrow = arrow;
		this.add(arrow);
		return this;
	}

	Map arrowLeft(){
		if(left == null){
			left = Arrow.getLeft(this);
			left.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					Map.this.translate(Direction.LEFT);
					Map.this.bringToFront(left);
				}
			});
		}
		return arrow(left);
	}

	Map arrowRight(){
		if(right == null){
			right = Arrow.getRight(this);
			right.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					Map.this.translate(Direction.RIGHT);
					Map.this.bringToFront(right);
				}
			});
		}
		return arrow(right);
	}

	Map arrowUp(){
		if(up == null){
			up = Arrow.getUp(this);
			up.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					Map.this.translate(Direction.UP);
					Map.this.bringToFront(up);
				}
			});
		}
		return arrow(up);
	}

	Map arrowDown(){
		if(down == null){
			down = Arrow.getDown(this);
			down.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					Map.this.translate(Direction.DOWN);
					Map.this.bringToFront(down);
				}
			});
		}
		return arrow(down);
	}

	Map arrowUpLeft(){
		if(upLeft == null){
			upLeft = Arrow.getUpLeft(this);
			upLeft.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					Map.this.translate(Direction.UPLEFT);
					Map.this.bringToFront(upLeft);
				}
			});
		}
		return arrow(upLeft);
	}

	Map arrowUpRight(){
		if(upRight == null){
			upRight = Arrow.getUpRight(this);
			upRight.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					Map.this.translate(Direction.UPRIGHT);
					Map.this.bringToFront(upRight);
				}
			});
		}
		return arrow(upRight);
	}

	Map arrowDownLeft(){
		if(downLeft == null){
			downLeft = Arrow.getDownLeft(this);
			downLeft.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					Map.this.translate(Direction.DOWNLEFT);
					Map.this.bringToFront(downLeft);
				}
			});
		}
		return arrow(downLeft);
	}

	Map arrowDownRight(){
		if(downRight == null){
			downRight = Arrow.getDownRight(this);
			downRight.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					Map.this.translate(Direction.DOWNRIGHT);
					Map.this.bringToFront(downRight);
				}
			});
		}
		return arrow(downRight);
	}

	void removeCurrentArrow(){
		if(currentArrow != null)
			this.remove(currentArrow);
	}

	/**
	 * Se connecte au serveur pour chercher toutes les informations nécessaires à la
	 * complétion de la carte
	 */
	private void connectMap(){
		new Connector("map/infos/3/0", this);
	}

	private enum BatimentType {COLONIE,VILLE};
	private enum LinkType {ROUTE, TRANSPORT, CARGO, VOILLIER};

	@Override
	public void callback(JavaScriptObject json) {
		if (json == null)
			displayError();
		else{
			VoleurPath p = null;
			MapInfos jmap = asMap(json);
			JsArrayInteger brs = jmap.getBrigands();
			for(int i = 0; i<brs.length(); i++){
				p = new BrigandPath();
				p.setFillColor("black");
				plateau.get(brs.get(i)-1).setVoleur(p);
				p.addClickHandler(new ClickHandler() {
					
					@Override
					public void onClick(ClickEvent event) {
						Map.this.mch.onBrigandClick(event);
					}
				});
			}

			JsArrayInteger prs = jmap.getPirates();
			for(int i = 0; i<prs.length(); i++){
				p = new PiratePath();
				p.setFillColor("black");
				plateau.get(prs.get(i)-1).setVoleur(p);
				p.addClickHandler(new ClickHandler() {
					
					@Override
					public void onClick(ClickEvent event) {
						Map.this.mch.onPirateClick(event);
					}
				});
			}

			JsArray<BatimentInfos> cols = jmap.getColonies();
			BatimentInfos col;
			for(int i = 0; i<cols.length(); i++){
				col = cols.get(i);
				addBatiment(col, BatimentType.COLONIE);
			}


			JsArray<BatimentInfos> vils = jmap.getVilles();
			BatimentInfos vil;
			for(int i = 0; i<vils.length(); i++){
				vil = vils.get(i);
				addBatiment(vil, BatimentType.VILLE);
			}



			JsArray<LienInfos> routs = jmap.getRoutes();
			LienInfos rout;
			for(int i = 0; i<routs.length(); i++){
				rout = routs.get(i);
				this.addLien(rout, LinkType.ROUTE);
			}

			/*
			 * Bateaux : on vérifie si deux bateaux n'ont pas la même 
			 * position, ils ne seront pas affichés pareils.
			 */
			JsArray<LienInfos> transp = jmap.getBateauxTransports();
			JsArray<LienInfos> cargs = jmap.getCargos();
			JsArray<LienInfos> voils = jmap.getVoilliers();
			
			
			ArrayList<LienInfos> transpSeuls = new ArrayList<LienInfos>();
			ArrayList<LienInfos> cargsSeuls = new ArrayList<LienInfos>();
			ArrayList<LienInfos> voilsSeuls = new ArrayList<LienInfos>();
			ArrayList<ArrayList<LienInfos>> batMultiples = new ArrayList<ArrayList<LienInfos>>();
			HashSet<Integer> deletedTransp = new HashSet<Integer>();
			HashSet<Integer> deletedCargs = new HashSet<Integer>();
			HashSet<Integer> deletedVoils = new HashSet<Integer>();
			
			
			ArrayList<LienInfos> mult = new ArrayList<LienInfos>();
			
			LienInfos li;
			for(int i = 0; i<transp.length(); i++){
				if(deletedTransp.contains(i))
					continue;
				li = transp.get(i);
				for(int j = i+1; j<transp.length(); j++){
					if (equalsPosBateaux(li, transp.get(j)))
					{
						deletedTransp.add(j);
						mult.add(transp.get(j));
					}
						
				}
				for(int j = 0; j<cargs.length(); j++){
					if (equalsPosBateaux(li, cargs.get(j)))
					{
						deletedCargs.add(j);
						mult.add(cargs.get(j));
					}
				}
				for(int j = 0; j<voils.length(); j++){
					if (equalsPosBateaux(li, voils.get(j)))
					{
						deletedVoils.add(j);
						mult.add(voils.get(j));
					}
				}
				
				if(mult.size() == 0)
					transpSeuls.add(li);
				else{
					mult.add(li);
					batMultiples.add(mult);
					mult = new ArrayList<LienInfos>();
				}
			}
			
			for(int i = 0; i<cargs.length(); i++){
				if(deletedCargs.contains(i))
					continue;
				
				li = cargs.get(i);
				for(int j = i+1; j<cargs.length(); j++){
					if (equalsPosBateaux(li, cargs.get(j)))
					{
						deletedCargs.add(j);
						mult.add(cargs.get(j));
					}
				}
				for(int j = 0; j<voils.length(); j++){
					if (equalsPosBateaux(li, voils.get(j)))
					{
						deletedVoils.add(j);
						mult.add(voils.get(j));
					}
				}
				
				if(mult.size() == 0)
					cargsSeuls.add(li);
				else{
					mult.add(li);
					batMultiples.add(mult);
					mult = new ArrayList<LienInfos>();
				}
			}
			
			for(int i = 0; i<voils.length(); i++){
				if(deletedVoils.contains(i))
					continue;
				li = voils.get(i);
				for(int j = i+1; j<voils.length(); j++){
					if (equalsPosBateaux(li, voils.get(j)))
					{
						deletedVoils.add(j);
						mult.add(voils.get(j));
					}
				}
				
				if(mult.size() == 0)
					voilsSeuls.add(li);
				else{
					mult.add(li);
					batMultiples.add(mult);
					mult = new ArrayList<LienInfos>();
				}
			}
			
			
			for(LienInfos trans : transpSeuls)
				this.addLien(trans,LinkType.TRANSPORT);

			for(LienInfos carg : cargsSeuls)
				this.addLien(carg,LinkType.CARGO);		
			for(LienInfos voil : voilsSeuls)
				this.addLien(voil,LinkType.VOILLIER);
			
			for(ArrayList<LienInfos> batMult : batMultiples){
				this.addBatMult(batMult);
			}
			
			draw();
		}
	}

	private boolean equalsPosBateaux(LienInfos li1, LienInfos li2){
		return (
				li1.getPosition1() == li2.getPosition1() 
				&& li1.getPosition2() == li2.getPosition2() )
				||
				(
				li1.getPosition2() == li2.getPosition1() 
					&& li1.getPosition1() == li2.getPosition2() 
					);
	}

	private void addBatiment(BatimentInfos bat, BatimentType type){
		PionJoueurPath pjp = null;
		switch(type){
		case COLONIE:{
			pjp = new ColoniePath(bat.getJoueur());
			pjp.addClickHandler(new ClickHandler() {
				
				@Override
				public void onClick(ClickEvent event) {
					Map.this.mch.onColonieClick(event);
				}
			});
			break;
		}
		case VILLE:{
			pjp = new VillePath(bat.getJoueur());
			pjp.addClickHandler(new ClickHandler() {
				
				@Override
				public void onClick(ClickEvent event) {
					Map.this.mch.onVilleClick(event);
				}
			});
			break;
		}

		}


		int[] tab = getHexagoneFromIntersection(bat.getPosition());
		if(tab[1] == 0)
			plateau.get(tab[0]-1).setIntLeft(pjp);
		else
			plateau.get(tab[0]-1).setIntRight(pjp);
		
		pjp.setFillColor(User.getPlayer(bat.getJoueur()).getColor().getColorCode());
	}

	private void addLien(LienInfos lien, LinkType type){
		int[] tab1 = getHexagoneFromIntersection(lien.getPosition1());
		int[] tab2 = getHexagoneFromIntersection(lien.getPosition2());

		SideDirection dir;
		int hex;


		if(tab1[0] == tab2[0]){
			dir = SideDirection.NONE;
			hex = tab1[0];
		}
		else{
			boolean tab1Left = tab1[1] == 0;
			boolean t1Abovt2 = (tab1[0] < tab2[0] || (tab1[0] >= 2*MAP_HW*(MAP_HH-1) 
					&& tab2[0] <= 2*MAP_HW));
			if(tab1Left){
				if(t1Abovt2){
					dir = SideDirection.LEFT;
					hex = tab1[0];
				}
				else{
					dir = SideDirection.RIGHT;
					hex = tab2[0];
				}
			}
			else{
				if(t1Abovt2){
					dir = SideDirection.RIGHT;
					hex = tab1[0];
				}
				else{
					dir = SideDirection.LEFT;
					hex = tab2[0];
				}
			}
		}

		PionJoueurPath pjp = null;
		switch(type){
		case ROUTE:{
			pjp = new RoutePath(lien.getJoueur(), dir);
			pjp.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					mch.onRouteClick(event);
				}
				
			});
			break;
		}
		case TRANSPORT:{
			pjp = new TransportPath(lien.getJoueur(), dir);
			pjp.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					mch.onBateauTransportClick(event);
				}
				
			});
			break;
		}
		case CARGO:{
			pjp = new CargoPath(lien.getJoueur(), dir);
			pjp.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					mch.onCargoClick(event);
				}
				
			});
			break;
		}
		case VOILLIER:{
			pjp = new VoilierPath(lien.getJoueur(), dir);
			pjp.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					mch.onVoilierClick(event);
				}
				
			});
			break;
		}

		}


		switch(dir){
		case LEFT:
			plateau.get(hex-1).setArLeft(pjp);
			break;
		case NONE:
			plateau.get(hex-1).setArUp(pjp);
			break;
		case RIGHT:
			plateau.get(hex-1).setArRight(pjp);
			break;

		}
		
		pjp.setFillColor(User.getPlayer(lien.getJoueur()).getColor().getColorCode());
	}
	

	private void addBatMult(ArrayList<LienInfos> batMult) {
		int[] tab1 = getHexagoneFromIntersection(batMult.get(0).getPosition1());
		int[] tab2 = getHexagoneFromIntersection(batMult.get(0).getPosition2());

		SideDirection dir;
		int hex;


		if(tab1[0] == tab2[0]){
			dir = SideDirection.NONE;
			hex = tab1[0];
		}
		else{
			boolean tab1Left = tab1[1] == 0;
			boolean t1Abovt2 = (tab1[0] < tab2[0] || (tab1[0] >= 2*MAP_HW*(MAP_HH-1) 
					&& tab2[0] <= 2*MAP_HW));
			if(tab1Left){
				if(t1Abovt2){
					dir = SideDirection.LEFT;
					hex = tab1[0];
				}
				else{
					dir = SideDirection.RIGHT;
					hex = tab2[0];
				}
			}
			else{
				if(t1Abovt2){
					dir = SideDirection.RIGHT;
					hex = tab1[0];
				}
				else{
					dir = SideDirection.LEFT;
					hex = tab2[0];
				}
			}
		}
		ArrayList<Integer> joueurs = new ArrayList<Integer>();
		for(LienInfos li : batMult)
			joueurs.add(li.getJoueur());
		
		BateauxGroup bat = new BateauxGroup(joueurs, dir);
		
		switch(dir){
		case LEFT:
			plateau.get(hex-1).setArLeft(bat);
			break;
		case NONE:
			plateau.get(hex-1).setArUp(bat);
			break;
		case RIGHT:
			plateau.get(hex-1).setArRight(bat);
			break;
		}
		
		bat.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(ClickEvent event) {
				mch.onBateauxMultipleClick(event);
			}
			
		});
		
		User me = User.getMe();
		if(joueurs.contains(me.getNumber())){
			bat.setFillColor(me.getColor().getColorCode());
		}
		else
			bat.setFillColor(User.getPlayer(batMult.get(0).getJoueur()).getColor().getColorCode());
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
