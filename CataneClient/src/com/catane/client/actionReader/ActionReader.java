package com.catane.client.actionReader;



import java.util.ArrayList;

import org.vaadin.gwtgraphics.client.DrawingArea;
import org.vaadin.gwtgraphics.client.shape.Rectangle;

import com.catane.client.map.Map;
import com.catane.client.requests.Connector;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;

public class ActionReader extends DrawingArea {

	final static double CENTER_RECT_OFFSET = 0.2;

	private static final int NB_DISPLAYED_ACTIONS = 4;
	private ArrayList<ActionGroup> actionGroups;

	private ActionReader() {
		super(Map.LITTLE_MAP_WIDTH, 350);
		this.add(new Rectangle(0, 0, getWidth(), getHeight()));


		int ml = (int)(getWidth()*CENTER_RECT_OFFSET);
		int crw = getWidth() - 2*ml;
		int mu = (int)(getHeight()*CENTER_RECT_OFFSET);
		int crh = getHeight()-2*mu;
		Rectangle centerRect = new Rectangle(ml,mu,crw,crh);
		centerRect.setRoundedCorners(10);
		this.add(centerRect);

		arrows();

		actionGroups = new ArrayList<ActionGroup>();
		for(int i = 0; i<NB_DISPLAYED_ACTIONS; i++)
			actionGroups.add(new ActionGroup(this));

		this.add(actionGroups.get(0));
		int x = ml+10, y = mu+50;
		for(ActionGroup ag : actionGroups){
			ag.moveTo(x, y);
			y+=30;
		}


		ActionReaderConnectable arc = new ActionReaderConnectable(this);
		new Connector("arbre_actions", arc);

	}

	private static ActionReader inst;

	public static ActionReader getActionReader() {
		if(inst == null)
			inst = new ActionReader();
		return inst;
	}

	/**
	 * Indice de la première action affichée dans l'actionNode.
	 */
	private int fAcIndex;

	/**
	 * Position de la future action déposée. 
	 */
	private int posEmpty;

	private ActionNode node;

	void setActionNode(ActionNode a){
		if(a != null){
			node = a;
			int nb = a.getNbActions();
			int p = nb - (actionGroups.size()-1);

			if(p>=0){
				if(p!= 0)
					this.add(mup);
				fAcIndex = p;
			}
			else
			{
				fAcIndex = 0;
			}
			posEmpty = nb;
			drawActions();

			refreshArrows();
		}
	}

	private void drawActions(){
		ActionGroup ag;
		int p;
		for(int i = 0; i<actionGroups.size(); i++){
			p = i + fAcIndex;
			ag = actionGroups.get(i);
			if(p == posEmpty){
				ag.setAction(null);
			}
			else 
			{
				if(p>posEmpty)
					p--;
				if(p >= node.getNbActions()){
					for(int j = i;j<actionGroups.size(); j++)
						if(ag.getParent() == this)
							this.remove(ag);
					break;
				}
				ag.setAction(node.getAction(p));
			}
			if(ag.getParent() != this)
				this.add(ag);
		}
		
	}

	private void listDown(){
		fAcIndex++;
		if(fAcIndex < node.getNbActions()-(actionGroups.size()-1) && mdown.getParent()!=this)
			this.add(mdown);
		if(fAcIndex >= node.getNbActions()-(actionGroups.size()-1) && mdown.getParent()==this)
			this.remove(mdown);
		if(mup.getParent()!=this)
			this.add(mup);
		drawActions();
	}

	private void listUp(){
		fAcIndex--;
		if(fAcIndex != 0 && mup.getParent()!=this)
			this.add(mup);
		if(fAcIndex == 0 && mup.getParent()==this)
			this.remove(mup);
		if(mdown.getParent()!=this)
			this.add(mdown);
		drawActions();
	}

	void moveEmptyUp(){
		if(posEmpty!=0){
			posEmpty--;
			if(posEmpty<fAcIndex)
				fAcIndex--;
			drawActions();
		}
	}

	void moveEmptyDown(){
		if(posEmpty != node.getNbActions()){
			posEmpty++;
			if(posEmpty>=fAcIndex+actionGroups.size())
				fAcIndex++;
			drawActions();
		}
	}


	/* -------------------------------------------- FLECHES --------------------------------*/

	private void arrows(){
		arrowLeft();
		arrowRight();
		arrowUp();
		arrowDown();
		arrowMUp();
		arrowMDown();
	}

	/* -------------------------------------------- FLECHES INTERIEURES --------------------------------*/
	private Arrow mup;
	private Arrow mdown;


	void arrowMUp(){
		if(mup == null){
			mup = Arrow.getMUp(this);
			mup.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					listUp();
				}
			});
		}
	}

	void arrowMDown(){
		if(mdown == null){
			mdown = Arrow.getMDown(this);
			mdown.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					listDown();
				}
			});
		}
	}

	/* -------------------------------------------- FLECHES EXTERIEURES --------------------------------*/

	private Arrow left;
	private Arrow right;
	private Arrow up;
	private Arrow down;
	
	private void refreshArrows(){
		refreshArrow(left);
		refreshArrow(right);
		refreshArrow(up);
		refreshArrow(down);
	}
	
	private void refreshArrow(Arrow ar){
		
		if(getNode(ar) == null){
			if(ar.getParent() == this)
				this.remove(ar);
		}
		else{
			if(ar.getParent() != this)
				this.add(ar);
		}
	}
	
	private ActionNode getNode(Arrow ar){
		if(ar == left)
			return node.getFather();
		else if(ar == right)
			return node.getFson();
		else if(ar == up)
			return node.getPsib();
		else if(ar == down)
			return node.getNsib();
		else
			return null;
	}
	
	void arrowLeft(){
		if(left == null){
			left = Arrow.getLeft(this);
			left.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					ActionReader.this.setActionNode(getNode(left));
				}
			});
		}
		this.add(left);
	}

	void arrowRight(){
		if(right == null){
			right = Arrow.getRight(this);
			right.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					ActionReader.this.setActionNode(getNode(right));
				}
			});
		}
		this.add(right);
	}

	void arrowUp(){
		if(up == null){
			up = Arrow.getUp(this);
			up.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					ActionReader.this.setActionNode(getNode(up));
				}
			});
		}
		this.add(up);
	}

	void arrowDown(){
		if(down == null){
			down = Arrow.getDown(this);
			down.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					ActionReader.this.setActionNode(getNode(down));
				}
			});
		}
		this.add(down);
	}



}


