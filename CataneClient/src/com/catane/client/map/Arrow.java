package com.catane.client.map;

import org.vaadin.gwtgraphics.client.shape.Path;


class Arrow extends Path {

	private Arrow(int x, int y) {
		super(x, y);
		this.setFillColor("white");
		this.setFillOpacity(0.5);
	}
	
	private static final int ARROW_PADDING = 10;
	private static final int ARROW_WIDTH = 30;
	private static final int ARROW_MARGIN = 50;
	
	public static Arrow getLeft(Map map){
		Arrow a = new Arrow(ARROW_PADDING,map.getHeight()/2);
		a.lineRelativelyTo(ARROW_WIDTH,-ARROW_WIDTH);
		a.lineRelativelyTo(0,2*ARROW_WIDTH);
		a.close();
		a.moveTo(0, ARROW_MARGIN);
		a.lineTo(ARROW_MARGIN, ARROW_MARGIN);
		a.lineTo(ARROW_MARGIN, map.getHeight()-ARROW_MARGIN);
		a.lineTo(0, map.getHeight()-ARROW_MARGIN);
		a.close();
		return a;
	}
	
	public static Arrow getRight(Map map){
		Arrow a = new Arrow(map.getWidth()-ARROW_PADDING,map.getHeight()/2);
		a.lineRelativelyTo(-ARROW_WIDTH,-ARROW_WIDTH);
		a.lineRelativelyTo(0,2*ARROW_WIDTH);
		a.close();
		a.moveTo(map.getWidth(), ARROW_MARGIN);
		a.lineTo(map.getWidth()-ARROW_MARGIN, ARROW_MARGIN);
		a.lineTo(map.getWidth()-ARROW_MARGIN, map.getHeight()-ARROW_MARGIN);
		a.lineTo(map.getWidth(), map.getHeight()-ARROW_MARGIN);
		a.close();
		return a;
	}
	
	public static Arrow getUp(Map map){
		Arrow a = new Arrow(map.getWidth()/2,ARROW_PADDING);
		a.lineRelativelyTo(-ARROW_WIDTH,ARROW_WIDTH);
		a.lineRelativelyTo(2*ARROW_WIDTH,0);
		a.close();
		a.moveTo(ARROW_MARGIN,0);
		a.lineTo(ARROW_MARGIN, ARROW_MARGIN);
		a.lineTo(map.getWidth()-ARROW_MARGIN, ARROW_MARGIN);
		a.lineTo(map.getWidth()-ARROW_MARGIN,0);
		a.close();
		return a;
	}
	
	public static Arrow getDown(Map map){
		Arrow a = new Arrow(map.getWidth()/2,map.getHeight()-ARROW_PADDING);
		a.lineRelativelyTo(-ARROW_WIDTH,-ARROW_WIDTH);
		a.lineRelativelyTo(2*ARROW_WIDTH,0);
		a.close();
		a.moveTo(ARROW_MARGIN,map.getHeight());
		a.lineTo(ARROW_MARGIN, map.getHeight()-ARROW_MARGIN);
		a.lineTo(map.getWidth()-ARROW_MARGIN, map.getHeight()-ARROW_MARGIN);
		a.lineTo(map.getWidth()-ARROW_MARGIN,map.getHeight());
		a.close();
		return a;
	}
	
	public static Arrow getUpLeft(Map map){
		Arrow a = new Arrow(ARROW_PADDING,ARROW_PADDING);
		a.lineRelativelyTo(0,ARROW_WIDTH);
		a.lineRelativelyTo(ARROW_WIDTH,-ARROW_WIDTH);
		a.close();
		a.moveTo(0,0);
		a.lineTo(0,ARROW_MARGIN);
		a.lineTo(ARROW_MARGIN,ARROW_MARGIN);
		a.lineTo(ARROW_MARGIN,0);
		a.close();
		return a;
	}
	
	public static Arrow getUpRight(Map map){
		Arrow a = new Arrow(map.getWidth()-ARROW_PADDING,ARROW_PADDING);
		a.lineRelativelyTo(-ARROW_WIDTH,0);
		a.lineRelativelyTo(ARROW_WIDTH,ARROW_WIDTH);
		a.close();
		a.moveTo(map.getWidth(),ARROW_MARGIN);
		a.lineTo(map.getWidth(),0);
		a.lineTo(map.getWidth()-ARROW_MARGIN,0);
		a.lineTo(map.getWidth()-ARROW_MARGIN,ARROW_MARGIN);
		a.close();
		return a;
	}
	
	public static Arrow getDownLeft(Map map){
		Arrow a = new Arrow(ARROW_PADDING,map.getHeight()-ARROW_PADDING);
		a.lineRelativelyTo(ARROW_WIDTH,0);
		a.lineRelativelyTo(-ARROW_WIDTH,-ARROW_WIDTH);
		a.close();
		a.moveTo(0,map.getHeight()-ARROW_MARGIN);
		a.lineTo(0,map.getHeight());
		a.lineTo(ARROW_MARGIN,map.getHeight());
		a.lineTo(ARROW_MARGIN,map.getHeight()-ARROW_MARGIN);
		a.close();
		return a;
	}
	
	public static Arrow getDownRight(Map map){
		Arrow a = new Arrow(map.getWidth()-ARROW_PADDING,map.getHeight()-ARROW_PADDING);
		a.lineRelativelyTo(-ARROW_WIDTH,0);
		a.lineRelativelyTo(ARROW_WIDTH,-ARROW_WIDTH);
		a.close();
		a.moveTo(map.getWidth(),map.getHeight()-ARROW_MARGIN);
		a.lineTo(map.getWidth(),map.getHeight());
		a.lineTo(map.getWidth()-ARROW_MARGIN,map.getHeight());
		a.lineTo(map.getWidth()-ARROW_MARGIN,map.getHeight()-ARROW_MARGIN);
		a.close();
		return a;
	}
	
}
