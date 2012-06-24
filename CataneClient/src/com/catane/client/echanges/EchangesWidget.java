package com.catane.client.echanges;

import org.vaadin.gwtgraphics.client.DrawingArea;
import org.vaadin.gwtgraphics.client.shape.Circle;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.VerticalPanel;

public class EchangesWidget extends Composite{

	public EchangesWidget() {
		VerticalPanel vp = new VerticalPanel();


		final DrawingArea canvas = new DrawingArea(500, 500);
		final Circle circle = new Circle(200, 200, 50);
		canvas.add(circle);
		vp.add(canvas);
		Button b1 = new Button("Hide");
		Button b2 = new Button("Show");
		vp.add(b1);
		vp.add(b2);
		b1.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				circle.removeFromParent();
			}
		});
		b2.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				canvas.add(circle);
			}
		});


		initWidget(vp);
	}
}

