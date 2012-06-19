package com.catane.client.actions;

import com.catane.client.Ressources;
import com.catane.client.map.Terre;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.Widget;

public class JouerDecouverte extends Action {

	private static final String TITLE = "Développement : Découverte";
	
	private Ressources res1, res2;
	private Terre terre;
	public JouerDecouverte(Terre terre, Ressources res1, Ressources res2) {
		super(TITLE);
		this.terre =terre;
		this.res1 = res1;
		this.res2 = res2;
		init();
	}

	@Override
	protected Widget getPopupWidget() {
		return new PopupWidget();
	}
	
	class PopupWidget extends Composite{
		private Label l;
		public PopupWidget() {
			l = new Label("Decouverte sur "+terre.getName()+" : "+res1+" "+res2);
			this.initWidget(l);
		}
	}

}
