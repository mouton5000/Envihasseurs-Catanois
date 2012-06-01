package com.catane.client.infosWidgets;


import com.catane.client.requests.Connectable;
import com.catane.client.requests.Connector;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;

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
		
		
		hP.add(rArg);
		hP.add(rBle);
		hP.add(rBoi);
		hP.add(rCai);
		hP.add(rMou);
		hP.add(rOr);
		hP.add(points);
		hP.add(Voleur);
		
		initWidget(hP);
		refreshInfos();
	}

	private void refreshInfos() {
		new Connector("ressources/infos/3/0/1", new Connectable(){

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
