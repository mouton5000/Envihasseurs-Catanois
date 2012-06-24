package com.catane.client;


import com.catane.client.actionReader.ActionReader;
import com.catane.client.bateaux.BateauxWidget;
import com.catane.client.constructions.ConstructionsWidget;
import com.catane.client.developpements.DeveloppementWidget;
import com.catane.client.echanges.EchangesWidget;
import com.catane.client.genInfos.GenInfoWidget;
import com.catane.client.infosWidgets.InfoWidget;
import com.catane.client.map.Map;
import com.catane.client.map.MapWidget;
import com.catane.client.map.Terre;
import com.catane.client.options.OptionsWidget;
import com.catane.client.points.PointsWidget;
import com.catane.client.requests.Connectable;
import com.catane.client.requests.Connector;
import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;
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

	public static CataneClient instance;
	
	/**
	 * This is the entry point method.
	 */
	public void onModuleLoad() {
		instance = this;
		
		new Connector("players/all",new Connectable() {

			@Override
			public void displayError() {

				secondStep();
			}

			@Override
			public void callback(JavaScriptObject json) {
				int meIndex = asMeIndex(json);
				JsArray<UserInfos> users = asArrayOfUsers(json);
								
				User.meIndex = meIndex;
				UserInfos ui;

				for(int i = 0; i<users.length(); i++){
					ui = users.get(i);
					User.users.add(new User(ui.getNumber(), ui.getColor(), ui.getUsername()));
				}

				secondStep();
			}
			
			private final native JsArray<UserInfos> asArrayOfUsers(JavaScriptObject json)/*-{
	    		return json.users;
	  		}-*/;
			
			private final native int asMeIndex(JavaScriptObject json)/*-{
    			return json.meIndex;
  			}-*/;

		});
		

	}
	
	public InfoWidget info;
	public MapWidget map;
	public ActionReader actionReader;
	public TabPanel rightPanel;
	
	
	private void secondStep() {
		Terre.makeTerres();

		Panel infoPanel = new HorizontalPanel();
		Panel centerPanel = new HorizontalPanel();
		Panel leftPanel = new VerticalPanel();
		//Panel rightPanel = new VerticalPanel();
		rightPanel = new TabPanel();

		DockPanel dockPanel = new DockPanel();

		info = new InfoWidget();
		map = new MapWidget();
		actionReader = ActionReader.getActionReader();



		leftPanel.add(map);
		leftPanel.add(actionReader);
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
		
		
		
		refreshAll();
	}
	
	/**
	 * Rafraichissement quand on modifie la terre choisie.
	 */
	public void refreshFromTerre(){
		info.refreshInfos();
		Map.getLittleMap().draw();
	}
	
	/**
	 * Rafraichissement quand on déplace l'action vide
	 */
	public void refreshMoveEmptyNode(){
		info.refreshInfos();
		Map.getLittleMap().refreshDiff();
	}
	
	/**
	 * Rafraichissement de tout.
	 */
	public void refreshAll(){
		info.refreshInfos();
		Map.getLittleMap().refresh();
	}
}

