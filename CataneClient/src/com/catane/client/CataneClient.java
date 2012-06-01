package com.catane.client;

import gwt.g2d.client.graphics.KnownColor;
import gwt.g2d.client.graphics.Surface;
import gwt.g2d.client.graphics.shapes.ShapeBuilder;

import com.catane.client.infosWidgets.InfoWidget;
import com.catane.client.map.Map;
import com.catane.client.map.MapWidget;
import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.DockPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Panel;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.TabPanel;
import com.google.gwt.user.client.ui.VerticalPanel;

/**
 * Entry point classes define <code>onModuleLoad()</code>.
 */
public class CataneClient implements EntryPoint {
	/**
	 * The message displayed to the user when the server cannot be reached or
	 * returns an error.
	 */
	
	/**
	 * This is the entry point method.
	 */
	public void onModuleLoad() {
		//		final TextBox nameField = new TextBox();
		//		final Label errorLabel = new Label();

		Panel infoPanel = new HorizontalPanel();
		Panel centerPanel = new HorizontalPanel();
		Panel leftPanel = new VerticalPanel();
		//Panel rightPanel = new VerticalPanel();
		TabPanel rightPanel = new TabPanel();

		DockPanel dockPanel = new DockPanel();


		final Button infoButton = new Button("Info");
		final InfoWidget info = new InfoWidget();
		final MapWidget map = new MapWidget();
		final Button actionsButton = new Button("actions");



		leftPanel.add(map);
		leftPanel.add(actionsButton);
		infoPanel.add(info);


		String[] menus = {"Infos Générales", "Constructions", "Bateaux", "Développement", "Points", "Echanges", "Options"};

		int i = 0;
		for(String s : menus){
			final Button rB = new Button(s);
			rightPanel.insert(rB, s, i);
			rB.setStyleName("tabButtonTest");
			i++;
		}

		rightPanel.selectTab(0);
		//rightPanel.add(rightButton);

		centerPanel.add(leftPanel);
		centerPanel.add(rightPanel);

		infoPanel.setStyleName("hPanel");
		centerPanel.setStyleName("hPanel");
		leftPanel.setStyleName("vPanel");
		rightPanel.setStyleName("vPanel");

		dockPanel.add(infoPanel, DockPanel.NORTH);
		dockPanel.add(leftPanel, DockPanel.WEST);
		dockPanel.add(rightPanel, DockPanel.EAST);

		dockPanel.setStyleName("hPanel");
		RootPanel.get().add(dockPanel);

		infoButton.setStyleName("buttonTest");
		actionsButton.setStyleName("buttonTest");


	}
}

