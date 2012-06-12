package com.catane.client;


import com.catane.client.bateaux.BateauxWidget;
import com.catane.client.constructions.ConstructionsWidget;
import com.catane.client.developpements.DeveloppementWidget;
import com.catane.client.echanges.EchangesWidget;
import com.catane.client.genInfos.GenInfoWidget;
import com.catane.client.infosWidgets.InfoWidget;
import com.catane.client.map.MapWidget;
import com.catane.client.options.OptionsWidget;
import com.catane.client.points.PointsWidget;
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

		Panel infoPanel = new HorizontalPanel();
		Panel centerPanel = new HorizontalPanel();
		Panel leftPanel = new VerticalPanel();
		//Panel rightPanel = new VerticalPanel();
		TabPanel rightPanel = new TabPanel();

		DockPanel dockPanel = new DockPanel();

		final InfoWidget info = new InfoWidget();
		final MapWidget map = new MapWidget();
		final Button actionsButton = new Button("actions");



		leftPanel.add(map);
		leftPanel.add(actionsButton);
		infoPanel.add(info);

		GenInfoWidget giw = new GenInfoWidget();
		ConstructionsWidget cw = new ConstructionsWidget();
		BateauxWidget bw =  new BateauxWidget();
		DeveloppementWidget dw = new DeveloppementWidget();
		PointsWidget pw = new PointsWidget();
		EchangesWidget ew = new EchangesWidget();
		OptionsWidget ow = new OptionsWidget();
		
		rightPanel.insert(giw, "Infos Générales", 0);
		rightPanel.insert(cw, "Constructions", 1);
		rightPanel.insert(bw, "Bateaux", 2);
		rightPanel.insert(dw, "Développement", 3);
		rightPanel.insert(pw, "Points", 4);
		rightPanel.insert(ew, "Echanges", 5);
		rightPanel.insert(ow, "Options", 6);
			

		rightPanel.selectTab(0);

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

		actionsButton.setStyleName("buttonTest");
		
		
//		new MapPopup().center();

	}
}

