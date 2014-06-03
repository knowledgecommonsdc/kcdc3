/**********************************************************


***********************************************************/

/* ---- PALETTE ---- */

@water:#474c52;
@land:#3c3c3c;
@building:#252525;
@road:#363636;
@railroad:#343434;

Map {
  background-color:@land;
}

#water,
#ocean {
  polygon-fill:@water;
  polygon-gamma:0.5; // reduces gaps between shapes
}




// modern features

#railroad {
  ::line, ::hatch { line-color: @railroad; }
  ::line { line-width:1; }
  ::hatch {
    line-width: 3;
    line-dasharray: 1, 14;
  }
}

#waterply {
  line-color:@water;
  line-width:0;
  polygon-opacity:1;
  polygon-fill:@water;
}

#bldgply {
  polygon-opacity:1;
  polygon-fill:@building;
  [zoom<=14] {
	line-width:0;
  }
}


