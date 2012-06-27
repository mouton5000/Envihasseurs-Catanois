package com.catane.client.map;

import java.util.ArrayList;

import org.vaadin.gwtgraphics.client.DrawingArea;
import org.vaadin.gwtgraphics.client.VectorObject;

import com.catane.client.actions.Action;
import com.catane.client.requests.Connector;
import com.catane.shared.Math2;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;



public class Map extends DrawingArea {


	/**
	 * Nombres d'hexagones sur une ligne de la carte
	 */
	public static final int MAP_HW = 5;

	/**
	 * Nombres d'hexagones sur une colone de la carte
	 */
	public static final int MAP_HH = 6;


	private MapMouseHandler mmh;
	MapClickHandler mch; 
	MapRefreshConnectable mrc;
	MapDiffConnectable mdc;

	public Map(int width, int height) {
		super(width,height);

		mmh = new MapMouseHandler(this);
		this.addMouseMoveHandler(mmh);
		this.addMouseOutHandler(mmh);

		mrc = new MapRefreshConnectable(this);
		mdc = new MapDiffConnectable(this);

		buildPlateau();
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

			RoutePath rp;
			if((rp = hi.getRoutLeft()) != null){
				int x = coords[0]-getHLargeur()*3/2;
				int y = coords[1]-getHLongueur()/2;

				rp.setX(x);
				rp.setY(y);
				rp.setFillOpacity(opacity);
				if(rp.getParent() == null)
					this.add(rp);
			}

			if((rp = hi.getRoutUp()) != null){
				int x = coords[0];
				int y = coords[1]-getHLongueur();

				rp.setX(x);
				rp.setY(y);
				rp.setFillOpacity(opacity);
				if(rp.getParent() == null)
					this.add(rp);
			}

			if((rp = hi.getRoutRight()) != null){
				int x = coords[0]+getHLargeur()*3/2;
				int y = coords[1]-getHLongueur()/2;

				rp.setX(x);
				rp.setY(y);
				rp.setFillOpacity(opacity);
				if(rp.getParent() == null)
					this.add(rp);
			}



			VectorObject vo;
			if((vo = hi.getBatLeft()) != null){
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

			if((vo = hi.getBatUp()) != null){
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

			if((vo = hi.getBatRight()) != null){
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

	/**
	 * Supprime tous le pions.
	 */
	private void clearPions(){
		for(HexagoneInfos hi : plateau){
			VectorObject vo;
			if((vo = hi.getBatLeft()) != null){
				if(vo.getParent() == this){
					this.remove(vo);
				}
				hi.clearBatLeft();
			}
			if((vo = hi.getBatRight()) != null){
				if(vo.getParent() == this){
					this.remove(vo);
				}
				hi.clearBatRight();
			}
			if((vo = hi.getBatUp()) != null){
				if(vo.getParent() == this){
					this.remove(vo);
				}
				hi.clearBatUp();
			}
			if((vo = hi.getIntLeft()) != null){
				if(vo.getParent() == this){
					this.remove(vo);
				}
				hi.setIntLeft(null);
			}
			if((vo = hi.getIntRight()) != null){
				if(vo.getParent() == this){
					this.remove(vo);
				}
				hi.setIntRight(null);
			}
			if((vo = hi.getVoleur()) != null){
				if(vo.getParent() == this){
					this.remove(vo);
				}
				hi.setVoleur(null);
			}
		}
	}

	public void refresh(){
		clearPions();
		connectMap();
	}

	public void refreshDiff(){
		connectDiffMap();
	}

	void removeBatiment(int hex, int dir){
		HexagoneInfos hi = plateau.get(hex-1);
		VectorObject vo;
		if(dir == 0){
			if((vo = hi.getIntLeft()) != null){
				hi.setIntLeft(null);
				if(vo.getParent() == this)
					this.remove(vo);
			}
		}
		else
		{
			if((vo = hi.getIntRight()) != null){
				hi.setIntRight(null);
				if(vo.getParent() == this)
					this.remove(vo);
			}
		}
	}

	void removeRoute(int hex, SideDirection dir){
		HexagoneInfos hi = plateau.get(hex-1);
		VectorObject vo;
		switch(dir){
		case LEFT:
			if((vo = hi.getRoutLeft()) != null){
				hi.setRoutLeft(null);
				if(vo.getParent() == this)
					this.remove(vo);
			}
			break;
		case NONE:
			if((vo = hi.getRoutUp()) != null){
				hi.setRoutUp(null);
				if(vo.getParent() == this)
					this.remove(vo);
			}
			break;
		case RIGHT:
			if((vo = hi.getRoutRight()) != null){
				hi.setRoutRight(null);
				if(vo.getParent() == this)
					this.remove(vo);
			}
			break;

		}
	}

	void removeBateau(Bateau b, int hex, SideDirection dir){
		HexagoneInfos hi = plateau.get(hex-1);
		switch(dir){
		case LEFT: 
			hi.removeBatLeft(b);
			break;
		case NONE:
			hi.removeBatUp(b);
			break;
		case RIGHT:
			hi.removeBatRight(b);
			break;

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
	static int[] getHexagoneFromIntersection(int i){

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

		p = infos.getRoutLeft();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getRoutUp();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getRoutRight();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getBatLeft();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getBatUp();
		if(p != null && p.getParent() == this)
			this.remove(p);

		p = infos.getBatRight();
		if(p != null && p.getParent() == this)
			this.remove(p);
	}


	/*
	 * ------------------------------ FLECHES -------------------------------------
	 */

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


	/*
	 *  ---------------------------------- REQUETES -------------------------------
	 */

	/**
	 * Se connecte au serveur pour chercher les informations nécessaires à la
	 * complétion de toute la carte
	 */
	private void connectMap(){
		Action a = Action.getChosenOne();
		String urlAct = "";
		if(a!=null)
			urlAct += "/"+a.getNum();

		new Connector("map/infos"+urlAct, mrc);
	}

	/**
	 * Se connecte au serveur pour rafraichir les informations de la carte.
	 */
	private void connectDiffMap(){
		Action a = Action.getChosenOne(),
				p = Action.getPreviousOne();
		String urlAct = "";
		if(a!=null){

			if(p != null){
				urlAct += "/"+p.getNum();
			}
			urlAct += "/"+a.getNum();
		}
		else
			urlAct += "D/"+p.getNum();
		new Connector("map/diff"+urlAct, mdc);
	}


}

