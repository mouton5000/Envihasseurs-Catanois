package com.catane.client.map;

import org.vaadin.gwtgraphics.client.shape.Path;

public abstract class PionPath extends Path{
	
	private HexagoneInfos hi;
	
	public PionPath(int x, int y) {
		super(x, y);
	}
	
	public HexagoneInfos getHi() {
		return hi;
	}

	public void setHi(HexagoneInfos hi) {
		this.hi = hi;
	}

}
