package com.catane.client.requests;

import com.google.gwt.core.client.JavaScriptObject;

public interface Connectable {

	public void callback(JavaScriptObject json);
	public void displayError();
}
