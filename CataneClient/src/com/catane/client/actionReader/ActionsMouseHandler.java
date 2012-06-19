package com.catane.client.actionReader;

import com.google.gwt.event.dom.client.MouseMoveEvent;
import com.google.gwt.event.dom.client.MouseMoveHandler;
import com.google.gwt.event.dom.client.MouseOutEvent;
import com.google.gwt.event.dom.client.MouseOutHandler;

public class ActionsMouseHandler implements MouseMoveHandler, MouseOutHandler{

	private ActionReader ar;
	
	public ActionsMouseHandler(ActionReader ar) {
		this.ar = ar;
	}

	private boolean up = false;
	private boolean down = false;
	private boolean left = false;
	private boolean right = false;
	private boolean middle = false;
	
	/**
	 * Définit la valeur des 4 paramètres up, down, right et left. Chacun déclare
	 * que la souris est oui ou non proche du bord défini par la direction en question.
	 * Middle signifie que la souris est dans le carré central.
	 * @param up
	 * @param down
	 * @param left
	 * @param right
	 */
	private void setDir(boolean up, boolean down, boolean left, boolean right, boolean middle){
		this.up = up;
		this.down = down;
		this.left = left;
		this.right = right;
		this.middle = middle;
	}
	
	@Override
	public void onMouseMove(MouseMoveEvent event) {
		int x = event.getX();
		int y = event.getY();
		
		/**
		 * Limites pour l'affichage des flèches gauches et droites
		 */
		int xlL = 50,
				xrL = ar.getWidth()-50,
				ylruL = ar.getHeight()/2-30,
				ylrdL = ar.getHeight()/2+30;
		
		/**
		 * Limites pour l'affichage des flèches hautes et basses
		 */
		int yuL = 50,
				ydL = ar.getHeight()-50,
				xudlL = ar.getWidth()/2-30,
				xudrL = ar.getWidth()/2+30;
		
		int mu = (int)(ar.getHeight()*ActionReader.CENTER_RECT_OFFSET);
		int md = mu + ar.getHeight()-2*mu;
		/**
		 * Limites pour l'affichage des flèches milieu haut et bas
		 */
		int myuuL = mu,
			myudL = mu + 50,
			myduL = md - 50,
			myddL = md,
			mxudlL = ar.getWidth()/2-30,
			mxudrL = ar.getWidth()/2+30;
		
		
		
		boolean xl = x < xlL && y > ylruL && y < ylrdL,
				xr = x > xrL && y > ylruL && y < ylrdL,
				yu = y < yuL && x > xudlL && x < xudrL,
				yd = y > ydL && x > xudlL && x < xudrL,
				myu = y > myuuL && y < myudL && x > mxudlL && x < mxudrL,
				myd = y > myduL && y < myddL && x > mxudlL && x < mxudrL;
		
		
		if(!(right && !middle) && xr){
			setDir(false,false,false,true,false);
			ar.arrowRight();
		}
		else if(!(left && !middle) && xl){
			setDir(false,false,true,false,false);
			ar.arrowLeft();
		}
		else if(!(up && !middle) && yu){
			setDir(true,false,false,false,false);
			ar.arrowUp();
			
		}
		else if(!(down && !middle) && yd){
			setDir(false,true,false,false,false);
			ar.arrowDown();
		}
		else if(!(up && middle) && myu){
			setDir(true,false,false,false,true);
			ar.arrowMUp();
			
		}
		else if(!(down && middle) && myd){
			setDir(false,true,false,false,true);
			ar.arrowMDown();
		}
		else if((up || down || right || left) && !xr && !xl && !yd && !yu && !myu && !myd){
			setDir(false,false,false,false,false);
		}
	}

	@Override
	public void onMouseOut(MouseOutEvent event) {
		setDir(false,false,false,false,false);
	}

}
