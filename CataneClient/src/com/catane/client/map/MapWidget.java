package com.catane.client.map;

import com.gargoylesoftware.htmlunit.OnbeforeunloadHandler;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.VerticalPanel;


/**
 * Widget contenant la carte et les boutons qui vont avec.
 * @author mouton
 *
 */
public class MapWidget extends Composite implements ClickHandler{

	private Button leftB;
	private Button rightB;
	private Button upB;
	private Button downB;
	
	
	private Map map;

	public MapWidget() {
		map = Map.getLittleMap();

		HorizontalPanel hp = new HorizontalPanel();
		hp.add(map);

		VerticalPanel vp = new VerticalPanel();
		leftB = new Button("left");
		rightB = new Button("right");
		upB = new Button("up");
		downB = new Button("down");

		Button[] bs = {leftB, rightB, upB, downB};
		for(Button b : bs){
			vp.add(b);
			b.addClickHandler(this);
		}

		hp.add(vp);
		initWidget(hp);
	}

	@Override
	public void onClick(ClickEvent event) {
		Button b = (Button) event.getSource();
		if(b == leftB){
			map.left();
		}
		else if(b == rightB){
			map.right();
		}
		else if(b == upB){
			map.up();
		}
		else if(b == downB){
			map.down();
		}

	}

}
