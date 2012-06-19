package com.catane.client.infosWidgets;


import java.util.Iterator;

import com.catane.client.map.Map;
import com.catane.client.map.Terre;
import com.catane.client.requests.Connectable;
import com.catane.client.requests.Connector;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.ListBox;

/**
 * Désigne le widget d'information situé en haut de l'écran. Il donne entre autres
 * des informations comme la quantité de ressources du joueur, son classement et son nombre de points,
 * et si oui ou non il doit déplacer le voleur.
 * @author mouton
 *
 */
public class InfoWidget extends Composite {

	private RessourceInfoWidget rArg;
	private RessourceInfoWidget rBle;
	private RessourceInfoWidget rBoi;
	private RessourceInfoWidget rCai;
	private RessourceInfoWidget rMou;
	private RessourceInfoWidget rOr;

	private ListBox lb;
	public ListBox getLb(){
		return lb;
	}

	public InfoWidget() {
		super();

		rArg = RessourceInfoWidget.getArgile();
		rBle = RessourceInfoWidget.getBle();
		rBoi = RessourceInfoWidget.getBois();
		rCai = RessourceInfoWidget.getCaillou();
		rMou = RessourceInfoWidget.getMouton();
		rOr = RessourceInfoWidget.getOr();
		Label points = new Label("Points");
		Label Voleur = new Label("Voleur");

		HorizontalPanel hP = new HorizontalPanel();

		points.setStyleName("infosLabels");
		Voleur.setStyleName("infosLabels");

		lb = new ListBox();
		Iterator<Terre> it = Terre.getTerreIterator();
		while(it.hasNext())
			lb.addItem(it.next().getName());
		lb.addChangeHandler(new ChangeHandler() {

			@Override
			public void onChange(ChangeEvent event) {
				Terre t = Terre.getTerre(lb.getSelectedIndex());
				t.choose();
				Map.getLittleMap().center();
			}
		});

		hP.add(rArg);
		hP.add(rBle);
		hP.add(rBoi);
		hP.add(rCai);
		hP.add(rMou);
		hP.add(rOr);
		hP.add(points);
		hP.add(Voleur);
		hP.add(lb);

		initWidget(hP);
	}

	public void refreshInfos() {
		Terre t = Terre.getChosenOne();
		new Connector("ressources/infos/3/0/"+(t.getIndex()+1), new Connectable(){

			@Override
			public void callback(JavaScriptObject json) {
				if (json == null)
					displayError();
				else{
					RessourcesInfos jres = asRessources(json);
					InfoWidget.this.rArg.setValues(jres.getArgileLandValue(), jres.getArgileWorldValue());
					InfoWidget.this.rBle.setValues(jres.getBleLandValue(), jres.getBleWorldValue());
					InfoWidget.this.rBoi.setValues(jres.getBoisLandValue(), jres.getBoisWorldValue());
					InfoWidget.this.rCai.setValues(jres.getCaillouLandValue(), jres.getCaillouWorldValue());
					InfoWidget.this.rMou.setValues(jres.getMoutonLandValue(), jres.getMoutonWorldValue());
					InfoWidget.this.rOr.setValues(jres.getOrLandValue(), jres.getOrWorldValue());
				}
			}

			@Override
			public void displayError() {
				InfoWidget.this.rArg.displayError();
				InfoWidget.this.rBle.displayError();
				InfoWidget.this.rBoi.displayError();
				InfoWidget.this.rCai.displayError();
				InfoWidget.this.rMou.displayError();
				InfoWidget.this.rOr.displayError();
			}

			/**
			 * Cast JavaScriptObject as JsArray of StockData.
			 */
			private final native RessourcesInfos asRessources(JavaScriptObject jso) /*-{
			    return jso;
			  }-*/;

		});
	}

}
