package com.catane.client.actionReader;

import org.vaadin.gwtgraphics.client.shape.Path;

class Arrow extends Path {

	
	
	private Arrow(int x, int y) {
		super(x, y);
		this.setFillColor("white");
		this.setFillOpacity(0.5);
	}
	
	private static final int ARROW_PADDING = 10;
	private static final int ARROW_WIDTH = 30;
	
	public static Arrow getLeft(ActionReader ar){
		Arrow a = new Arrow(ARROW_PADDING,ar.getHeight()/2);
		a.lineRelativelyTo(ARROW_WIDTH,ARROW_WIDTH);
		a.lineRelativelyTo(0,-2*ARROW_WIDTH);
		a.close();
		a.moveRelativelyTo(-ARROW_PADDING, -ARROW_WIDTH-ARROW_PADDING);
		a.lineRelativelyTo(0, 2*ARROW_WIDTH+2*ARROW_PADDING);
		a.lineRelativelyTo(ARROW_WIDTH+2*ARROW_PADDING, 0);
		a.lineRelativelyTo(0, -2*ARROW_WIDTH-2*ARROW_PADDING);
		a.close();
		return a;
	}
	
	public static Arrow getRight(ActionReader ar){
		Arrow a = new Arrow(ar.getWidth()-ARROW_PADDING,ar.getHeight()/2);
		a.lineRelativelyTo(-ARROW_WIDTH,ARROW_WIDTH);
		a.lineRelativelyTo(0,-2*ARROW_WIDTH);
		a.close();
		a.moveRelativelyTo(ARROW_PADDING, -ARROW_WIDTH-ARROW_PADDING);
		a.lineRelativelyTo(0, 2*ARROW_WIDTH+2*ARROW_PADDING);
		a.lineRelativelyTo(-ARROW_WIDTH-2*ARROW_PADDING, 0);
		a.lineRelativelyTo(0, -2*ARROW_WIDTH-2*ARROW_PADDING);
		a.close();
		return a;
	}
	
	public static Arrow getUp(ActionReader ar){
		Arrow a = new Arrow(ar.getWidth()/2,ARROW_PADDING);
		a.lineRelativelyTo(ARROW_WIDTH,ARROW_WIDTH);
		a.lineRelativelyTo(-2*ARROW_WIDTH,0);
		a.close();
		a.moveRelativelyTo(-ARROW_WIDTH-ARROW_PADDING,-ARROW_PADDING);
		a.lineRelativelyTo(2*ARROW_WIDTH+2*ARROW_PADDING,0);
		a.lineRelativelyTo(0,ARROW_WIDTH+2*ARROW_PADDING);
		a.lineRelativelyTo(-2*ARROW_WIDTH-2*ARROW_PADDING,0);
		a.close();
		return a;
	}
	
	public static Arrow getDown(ActionReader ar){
		Arrow a = new Arrow(ar.getWidth()/2,ar.getHeight()-ARROW_PADDING);
		a.lineRelativelyTo(ARROW_WIDTH,-ARROW_WIDTH);
		a.lineRelativelyTo(-2*ARROW_WIDTH,0);
		a.close();
		a.moveRelativelyTo(-ARROW_WIDTH-ARROW_PADDING,ARROW_PADDING);
		a.lineRelativelyTo(2*ARROW_WIDTH+2*ARROW_PADDING,0);
		a.lineRelativelyTo(0,-ARROW_WIDTH-2*ARROW_PADDING);
		a.lineRelativelyTo(-2*ARROW_WIDTH-2*ARROW_PADDING,0);
		a.close();
		return a;
	}
	
	public static Arrow getMUp(ActionReader ar){
		Arrow a = new Arrow(ar.getWidth()/2,(int)(ar.getHeight()*ActionReader.CENTER_RECT_OFFSET));
		a.lineRelativelyTo(-ARROW_WIDTH,ARROW_WIDTH);
		a.lineRelativelyTo(2*ARROW_WIDTH,0);
		a.close();
		return a;
	}
	
	public static Arrow getMDown(ActionReader ar){
		Arrow a = new Arrow(ar.getWidth()/2,ar.getHeight()-(int)(ar.getHeight()*ActionReader.CENTER_RECT_OFFSET));
		a.lineRelativelyTo(-ARROW_WIDTH,-ARROW_WIDTH);
		a.lineRelativelyTo(2*ARROW_WIDTH,0);
		a.close();
		return a;
	}
	
	
	
}
