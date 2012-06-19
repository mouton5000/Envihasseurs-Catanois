package com.catane.client.actionReader;

import com.catane.client.actions.Action;
import com.catane.client.requests.Connectable;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.core.client.JsArrayString;

public class ActionReaderConnectable implements Connectable {

	private ActionReader ar;

	public ActionReaderConnectable(ActionReader ar) {
		this.ar = ar;
	}

	@Override
	public void callback(JavaScriptObject json) {
		JsArray<NodeInfos> niArray = asArrayOfNodeInfos(json);
		NodeInfos ni;
		ActionNode fan = null;
		for(int j = 0; j<niArray.length();j++){
			ni = niArray.get(j);
			ActionNode node = new ActionNode(ni.getNodeNum());
			node.setFather(ni.getFather());
			node.setFson(ni.getFirstChild());
			node.setPsib(ni.getPSibling()); 
			node.setNsib(ni.getSibling());

			JsArray<ActionInfos> actions = ni.getActions();
			ActionInfos ai;
			Action a;
			for(int i = 0; i<actions.length();i++){
				ai = actions.get(i);
				a = Action.getAction(ai.getFunc(), ai.getParams());
				node.addAction(a);
			}
			
			if(j == 0)
				fan = node;
		}
		ar.setActionNode(fan);

		
	}

	private final native JsArray<NodeInfos> asArrayOfNodeInfos(JavaScriptObject json) /*-{
		return json;
	}-*/;

	@Override
	public void displayError() {
	}

}

class NodeInfos extends JavaScriptObject{
	protected NodeInfos(){

	}

	public final native int getNodeNum() /*-{return this.num;}-*/;
	public final native int getFather() /*-{return this.father;}-*/;
	public final native int getFirstChild() /*-{return this.first_child;}-*/;
	public final native int getSibling() /*-{return this.sibling;}-*/;
	public final native int getPSibling() /*-{return this.pSibling;}-*/;

	public final native JsArray<ActionInfos> getActions() /*-{return this.actions;}-*/;
}

class ActionInfos extends JavaScriptObject{
	protected ActionInfos(){

	}

	public final native String getFunc() /*-{return this.func;}-*/;
	public final native JsArrayString getParams() /*-{return this.params;}-*/;
}