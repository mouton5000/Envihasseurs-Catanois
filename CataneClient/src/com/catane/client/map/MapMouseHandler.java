package com.catane.client.map;

import com.google.gwt.event.dom.client.MouseMoveEvent;
import com.google.gwt.event.dom.client.MouseMoveHandler;
import com.google.gwt.event.dom.client.MouseOutEvent;
import com.google.gwt.event.dom.client.MouseOutHandler;

public class MapMouseHandler implements MouseMoveHandler, MouseOutHandler{

	private Map map;
	
	public MapMouseHandler(Map map) {
		this.map = map;
	}

	private boolean up = false;
	private boolean down = false;
	private boolean left = false;
	private boolean right = false;
	
	/**
	 * Définit la valeur des 4 paramètres up, down, right et left. Chacun déclare
	 * que la souris est oui ou non proche du bord défini par la direction en question.
	 * @param up
	 * @param down
	 * @param left
	 * @param right
	 */
	private void setDir(boolean up, boolean down, boolean left, boolean right){
		this.up = up;
		this.down = down;
		this.left = left;
		this.right = right;
		
		
	}
	
	@Override
	public void onMouseMove(MouseMoveEvent event) {
		int x = event.getX();
		int y = event.getY();
		boolean xl = x < 50,
				xr = x > map.getWidth() - 50,
				yu = y < 50,
				yd = y > map.getHeight() - 50;
		
		
		if(xr){
			if(!(down && right) && yd){
				setDir(false,true,false,true);
				map.arrowDownRight();
			}
			else if(!(up && right) && yu){
				setDir(true,false,false,true);
				map.arrowUpRight();
			}
			else if(!right || !yd && down || !yu && up){
				setDir(false,false,false,true);
				map.arrowRight();
			}
		}
		else if(xl){
			if(!(down && left) && yd){
				setDir(false,true,true,false);
				map.arrowDownLeft();
			}
			else if(!(up && left) && yu){
				setDir(true,false,true,false);
				map.arrowUpLeft();
			}
			else if(!left || !yd && down || !yu && up){
				setDir(false,false,true,false);
				map.arrowLeft();
			}
		}
		else if(yd && (!down || !xl && left || !xr && right)){
			setDir(false,true,false,false);
			map.arrowDown();
		}
		else if(yu && (!up || !xl && left || !xr && right)){
			setDir(true,false,false,false);
			map.arrowUp();
		}
		else if((up || down || right || left) && !xr && !xl && !yd && !yu){
			setDir(false,false,false,false);
			map.removeCurrentArrow();
		}
	}

	@Override
	public void onMouseOut(MouseOutEvent event) {
		setDir(false,false,false,false);
		map.removeCurrentArrow();
	}

}
