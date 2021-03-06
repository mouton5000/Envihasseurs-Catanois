package com.catane.client.actions;

import com.catane.client.actions.DeplacerBateau.PopupWidget;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

public final class ConstruireBateau extends Action {

private static final String TITLE = "Construire bateau";
	
	private int position;
	private int num;
	public ConstruireBateau(int num, int position) {
		super(num, TITLE);
		this.position = position;
		this.num = num;
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
			l = new Label("Construction du bateau "+num+" en position "+position);
			b = new Button("Voir");
			VerticalPanel vp = new VerticalPanel();
			vp.add(l);
			vp.add(b);
			this.initWidget(vp);
		}
	}

}
