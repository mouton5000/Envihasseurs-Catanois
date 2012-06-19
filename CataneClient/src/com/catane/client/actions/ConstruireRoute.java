package com.catane.client.actions;

import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

public class ConstruireRoute extends Action{
	private static final String TITLE = "Construction : route";
	
	
	private int position;
	public ConstruireRoute(int position) {
		super(TITLE);
		this.position = position;
		
		init();
	}
	

	@Override
	protected Widget getPopupWidget() {
		return new PopupWidget();
	}
	
	class PopupWidget extends Composite{
		private Label l;
		private Button b;
		public PopupWidget() {
			l = new Label("Construction d'une route en position "+position);
			b = new Button("Voir");
			VerticalPanel vp = new VerticalPanel();
			vp.add(l);
			vp.add(b);
			this.initWidget(vp);
		}
	}
}
