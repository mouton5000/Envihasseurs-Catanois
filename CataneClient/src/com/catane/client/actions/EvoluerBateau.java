package com.catane.client.actions;

import com.catane.client.actions.DeplacerBateau.PopupWidget;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

public final class EvoluerBateau extends Action {

	private static final String TITLE = "Evoluer bateau";
	
	private int bnum;
	public EvoluerBateau(int num, int bnum) {
		super(num, TITLE);
		this.bnum = bnum;
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
			l = new Label("Evolution du bateau "+bnum);
			b = new Button("Voir");
			VerticalPanel vp = new VerticalPanel();
			vp.add(l);
			vp.add(b);
			this.initWidget(vp);
		}
	}

}
