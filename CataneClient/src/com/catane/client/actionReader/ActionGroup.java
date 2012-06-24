package com.catane.client.actionReader;

import org.vaadin.gwtgraphics.client.Group;
import org.vaadin.gwtgraphics.client.shape.Path;
import org.vaadin.gwtgraphics.client.shape.Rectangle;
import org.vaadin.gwtgraphics.client.shape.Text;

import com.catane.client.actions.Action;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.shared.HandlerRegistration;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.PopupPanel;

public class ActionGroup extends Group {

	private Text title;
	private Path deleteButton;
	private Path detailButton;
	private Path upButton;
	private Path downButton;
	private Rectangle contour;
	private ActionReader ar;

	private static final int TEXT_PADDING = 10;
	private static final int LEFT_PADDING = 10;
	private static final int RIGHT_PADDING = 10;
	private static final int WIDTH = 475;

	public ActionGroup(ActionReader ar){
		this(null,ar);
	}
	
	public ActionGroup(final Action action, final ActionReader ar) {
		this.ar = ar;
		this.title = new Text(TEXT_PADDING, TEXT_PADDING,"");
		this.deleteButton = new DeleteButton();
		this.detailButton = new DetailButton();
		this.upButton = new UpButton();
		this.downButton = new DownButton();
		this.contour = new Rectangle(0, -1, WIDTH-RIGHT_PADDING, 
				2*TEXT_PADDING +title.getTextHeight()+4);

		this.add(title);
		this.add(contour);
		
		this.upButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(ClickEvent event) {
				ar.moveEmptyUp();
			}
		});
		
		this.downButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(ClickEvent event) {
				ar.moveEmptyDown();
			}
		});
		
		setAction(action);
	}

	HandlerRegistration hrDelete;
	HandlerRegistration hrDetail;
	
	public void setAction(final Action action){
		if(hrDelete != null){
			hrDelete.removeHandler();
			hrDelete = null;
		}
		if(hrDetail != null){
			hrDetail.removeHandler();
			hrDetail = null;
		}
		if(action == null){
			this.title.setText("...");
			if(deleteButton.getParent() == this)
				this.remove(deleteButton);
			if(detailButton.getParent() == this)
				this.remove(detailButton);
			if(upButton.getParent() != this)
				this.add(upButton);
			if(downButton.getParent() != this)
				this.add(downButton);
		}
		else
		{
			if(deleteButton.getParent() != this)
				this.add(deleteButton);
			if(detailButton.getParent() != this)
				this.add(detailButton);
			if(upButton.getParent() == this)
				this.remove(upButton);
			if(downButton.getParent() == this)
				this.remove(downButton);
			
			this.title.setText(action.getTitle());

			hrDelete = this.deleteButton.addClickHandler(new ClickHandler() {

				@Override
				public void onClick(ClickEvent event) {
					PopupPanel pop = new PopupPanel(true);
					pop.setWidget(new Button("delete"));
					pop.center();
				}
			});

			hrDetail = this.detailButton.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					action.showPopup();
				}
			});
		}
	}

	public void moveTo(int x, int y){
		title.setX(x+TEXT_PADDING);
		title.setY(y-TEXT_PADDING+title.getTextHeight()+4);

		deleteButton.setX(x+WIDTH-RIGHT_PADDING-DeleteButton.WIDTH);
		deleteButton.setY(y+TEXT_PADDING);
		detailButton.setX(x+WIDTH-RIGHT_PADDING-DeleteButton.WIDTH-LEFT_PADDING-DetailButton.WIDTH); 
		detailButton.setY(y+TEXT_PADDING);
		upButton.setX(x+WIDTH-RIGHT_PADDING-DeleteButton.WIDTH);
		upButton.setY(y+TEXT_PADDING);
		downButton.setX(x+WIDTH-RIGHT_PADDING-DeleteButton.WIDTH-LEFT_PADDING-DetailButton.WIDTH); 
		downButton.setY(y+TEXT_PADDING);
		contour.setX(x);
		contour.setY(y-2);
		this.bringToFront(title);
	}


}

class DeleteButton extends Path{

	static final int WIDTH = 20;
	static final int HEIGHT = 20;

	public DeleteButton() {
		super(0,0);
		this.moveRelativelyTo(-WIDTH/2, -HEIGHT/2);
		this.lineRelativelyTo(0, HEIGHT);
		this.lineRelativelyTo(WIDTH, 0);
		this.lineRelativelyTo(0,-HEIGHT);
		this.close();
		this.setFillColor("red");
		
	}

}

class DetailButton extends Path{

	static final int WIDTH = 20;
	static final int HEIGHT = 20;

	public DetailButton() {
		super(0,0);
		this.moveRelativelyTo(-WIDTH/2, -HEIGHT/2);
		this.lineRelativelyTo(0, HEIGHT);
		this.lineRelativelyTo(WIDTH, 0);
		this.lineRelativelyTo(0,-HEIGHT);
		this.close();
		this.setFillColor("green");
	}

}


class UpButton extends Path{

	static final int WIDTH = 20;
	static final int HEIGHT = 20;

	public UpButton() {
		super(0,0);
		this.moveRelativelyTo(0, -HEIGHT/2+1);
		this.lineRelativelyTo(-WIDTH/2+1, HEIGHT-2);
		this.lineRelativelyTo(WIDTH-2, 0);
		this.close();
		this.moveRelativelyTo(-WIDTH/2, -1);
		this.lineRelativelyTo(0, HEIGHT);
		this.lineRelativelyTo(WIDTH, 0);
		this.lineRelativelyTo(0,-HEIGHT);
		this.close();
	}

}

class DownButton extends Path{

	static final int WIDTH = 20;
	static final int HEIGHT = 20;

	public DownButton() {
		super(0,0);
		this.moveRelativelyTo(0, HEIGHT/2-1);
		this.lineRelativelyTo(WIDTH/2-1, -HEIGHT+2);
		this.lineRelativelyTo(-WIDTH+2, 0);
		this.close();
		this.moveRelativelyTo(-WIDTH/2, -HEIGHT+1);
		this.lineRelativelyTo(0, HEIGHT);
		this.lineRelativelyTo(WIDTH, 0);
		this.lineRelativelyTo(0,-HEIGHT);
		this.close();
	}

}


