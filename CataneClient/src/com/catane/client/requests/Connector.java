package com.catane.client.requests;


import com.google.gwt.http.client.URL;

public class Connector {

	private static final String JSON_URL = "http://127.0.0.1:5000/";
	private static int jsonRequestId = 0;

	
	public Connector(String urlPath, Connectable handler) {
		this(urlPath, "", handler);
	}
	
	/**
	 * 
	 */
	public Connector(String urlPath, String urlOptions, Connectable handler) {
		
		String url = JSON_URL+urlPath+'?'+urlOptions;
		url = URL.encode(url) + (urlOptions.equals("")?"":"&")+"callback=";
	
		getJson(jsonRequestId++, url, handler);

	}

	/**
	 * Make call to remote server.
	 */
	public native static void getJson(int requestId, String url, Connectable handler) /*-{
	   var callback = "callback" + requestId;

	   // [1] Create a script element.
	   var script = document.createElement("script");
	   script.setAttribute("src", url+callback);
	   script.setAttribute("type", "text/javascript");

	   // [2] Define the callback function on the window object.
	   window[callback] = function(jsonObj) {
	   // [3]
	     handler.@com.catane.client.requests.Connectable::callback(Lcom/google/gwt/core/client/JavaScriptObject;)(jsonObj);
	     window[callback + "done"] = true;
	   }

	   // [4] JSON download has 1-second timeout.
	   setTimeout(function() {
	     if (!window[callback + "done"]) {
	       handler.@com.catane.client.requests.Connectable::displayError()();
	     }

	     // [5] Cleanup. Remove script and callback elements.
	     document.body.removeChild(script);
	     delete window[callback];
	     delete window[callback + "done"];
	   }, 10000);

	   // [6] Attach the script element to the document body.
	   document.body.appendChild(script);
	  }-*/;

}
