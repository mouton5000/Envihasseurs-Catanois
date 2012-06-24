package com.catane.client.bateaux;

import com.catane.client.requests.Connectable;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.VerticalPanel;

public class BateauxWidget extends Composite implements Connectable{

	private int bT,cT,vT;
	
	private Label bTL, cTL, vTL;
	
	
	public BateauxWidget() {
		VerticalPanel vp = new VerticalPanel();
		
		bTL = new Label();
		cTL = new Label();
		vTL = new Label();
	
		Button bB = new Button("+ bateau");
		Button cB = new Button("+ cargo");
		Button vB = new Button("+ voillier");
		
		refreshLabels();
		
		vp.add(bTL);
		vp.add(bB);
		vp.add(cTL);
		vp.add(cB);
		vp.add(vTL);
		vp.add(vB);
		
		connectBat();
		initWidget(vp);
	}


	private void refreshLabels() {
		bTL.setText("Bateaux Transports : "+bT);
		cTL.setText("Cargos : "+cT);
		vTL.setText("Voilleirs : "+vT);
		
	}
	
	private void connectBat() {
//		new Connector("constructions/3/0/1", this);
	}


	@Override
	public void callback(JavaScriptObject json) {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void displayError() {
		// TODO Auto-generated method stub
		
	}
}
