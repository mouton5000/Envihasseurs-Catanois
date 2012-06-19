package com.catane.client;

import gwt.g2d.client.graphics.Color;

import java.util.ArrayList;

import com.google.gwt.core.client.JavaScriptObject;

public class User {

	private int number;
	private Color color;
	private String username;


	public int getNumber() {
		return number;
	}

	public Color getColor() {
		return color;
	}

	public String getUsername() {
		return username;
	}
	
	public User() {
	}

	public User(int number, Color color, String username) {
		super();
		this.number = number;
		this.color = color;
		this.username = username;
	}

	static ArrayList<User> users = new ArrayList<User>();
	static Integer meIndex; 
	public static User getMe(){
		if (meIndex == null)
			return null;
		return users.get(meIndex-1);
	}
	
	public static User getPlayer(int nb){
		if(users.size() < nb)
			return null;
		return users.get(nb-1);
	}

}

class UserInfos extends JavaScriptObject{
	protected UserInfos(){
		
	}
	
	public final native int getNumber() /*-{return this.number}-*/;
	
	public final native int getRed() /*-{return this.red}-*/;
	public final native int getBlue() /*-{return this.blue}-*/;
	public final native int getGreen() /*-{return this.green}-*/;
	
	public final Color getColor(){
		return new Color(getRed(), getGreen(), getBlue());
	}
	public final native String getUsername() /*-{return this.username}-*/;
}
