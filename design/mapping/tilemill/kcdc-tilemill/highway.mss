@motorway:  @road;
@trunk:     @motorway;
@primary:   @road;
@secondary: @primary;
@road:      @road;
@track:     @road;
@footway:   @road;
@cycleway:  @road;

#highway::line {
  line-color: @road;
  line-width: 0;
  [highway='motorway'],
  [highway='trunk'] {
    [zoom=12] { line-width: 1.5; }
    [zoom=13] { line-width: 1.5; }
  }
  [highway='primary'],
  [highway='secondary'] {
    [zoom=12] { line-width: 1.5; }
    [zoom=13] { line-width: 1.5; }
  }
  [highway='motorway_link'],
  [highway='trunk_link'],
  [highway='primary_link'],
  [highway='secondary_link'],
  [highway='tertiary'],
  [highway='tertiary_link'],
  [highway='unclassified'],
  [highway='residential'],
  [highway='living_street'],
  [highway='service']{
    [zoom=12] { line-width: 1.0; }
    [zoom=13] { line-width: 1.0; }
  }
}

/*
#highway::line {
  [zoom>=8][zoom<=12] {
    [highway='motorway'] { line-color:@motorway; }
    [highway='trunk'] { line-color:@trunk; }
    [highway='motorway'],
    [highway='trunk'] {
      line-cap:round;
      line-join:round;
      [zoom=11] { line-width:2; }
    }
  }
  [zoom=11] {
    [highway='primary'] { line-color:@primary; }
    [highway='secondary'] { line-color:@secondary; }
    [highway='primary'],
    [highway='secondary'] {
      line-cap:round;
      line-join:round;
      [zoom=11] { line-width:1.5; }
    }
  }
  [zoom>=12][zoom<=13] {
    [highway='motorway_link'],
    [highway='trunk_link'],
    [highway='primary_link'],
    [highway='secondary_link'],
    [highway='tertiary'],
    [highway='tertiary_link'],
    [highway='unclassified'],
    [highway='residential'],
    [highway='living_street'] {
      line-color:@road;
      [zoom=12] { line-width:0.5; }
    }
  }
  [zoom>=14][zoom<=15] {
    [highway='service'],
    [highway='pedestrian'] {
      line-color:@road;
      [zoom=14] { line-width:0.5; }
    }
  }
  [zoom>=14] {
    [highway='track'],
    [highway='footway'],
    [highway='bridleway'] {
      line-color:@footway;
      line-dasharray:4,1;
      line-cap:butt;
      [zoom=16] { line-width:1.2; }
      [zoom=17] { line-width:1.6; }
      [zoom>17] { line-width:2; }
    }
    [highway='steps'] {
      line-color:@footway;
      line-dasharray:2,2;
      line-cap:butt;
      [zoom=16] { line-width:2; }
      [zoom=17] { line-width:3; }
      [zoom>17] { line-width:4; }
    }
    [highway='cycleway'] {
      line-color: @cycleway;
      line-dasharray:4,1;
      line-cap:butt;
      [zoom=16] { line-width:1.2; }
      [zoom=17] { line-width:1.6; }
      [zoom>17] { line-width:2; }
    }
  }
}

#motorways::case[zoom>=6][zoom<=12],
#mainroads::case[zoom>=10][zoom<=12],
#roads::case[zoom>=13][tunnel!=1][bridge!=1],
#tunnels::case[zoom>=13][tunnel=1],
#bridges::case[zoom>=13][bridge=1] {
  // -- line style --
  line-cap:round;
  line-join:round;
  line-width:0;
  [tunnel=1] {
    line-cap:butt;
    line-dasharray:6,3;
  }
  [bridge=1] { line-color:@road * 0.8; }
  // -- colors --
  line-color:@road;
  [highway='motorway'],
  [highway='motorway_link'] {
    line-color:@motorway;
    [bridge=1] { line-color:@motorway * 0.8; }
  }
  [highway='trunk'],
  [highway='trunk_link'] {
    line-color:@trunk;
    [bridge=1] { line-color:@trunk * 0.8; }
  }
  [highway='primary'],
  [highway='primary_link'] {
    line-color:@primary;
    [bridge=1] { line-color:@primary * 0.8; }
  }
  [highway='secondary'],
  [highway='secondary_link'] {
    line-color:@secondary;
    [bridge=1] { line-color:@secondary * 0.8; }
  }
  // -- widths --
  [highway='motorway'],
  [highway='trunk'] {
    [zoom=12] { line-width: 1.2 + 2; }
    [zoom=13] { line-width: 2 + 2; }
    [zoom=14] { line-width: 4 + 2; }
    [zoom=15] { line-width: 4 + 2; }
    [zoom=16] { line-width: 5 + 2; }
    [zoom=17] { line-width: 13 + 3; }
    [zoom>17] { line-width: 15 + 3; }
  }
  [highway='primary'],
  [highway='secondary'] {
    [zoom=12] { line-width: 1 + 2; }
    [zoom=13] { line-width: 1.2 + 2; }
    [zoom=14] { line-width: 2 + 2; }
    [zoom=15] { line-width: 4 + 2; }
    [zoom=16] { line-width: 7 + 3; }
    [zoom=17] { line-width: 9 + 3; }
    [zoom>17] { line-width: 11 + 3; }
  }
  [highway='motorway_link'],
  [highway='trunk_link'],
  [highway='primary_link'],
  [highway='secondary_link'],
  [highway='tertiary'],
  [highway='tertiary_link'],
  [highway='unclassified'],
  [highway='residential'],
  [highway='living_street'] {
    [zoom=14] { line-width: 1.6 + 1.6; }
    [zoom=15] { line-width: 4 + 2; }
    [zoom=16] { line-width: 6 + 2; }
    [zoom=17] { line-width: 8 + 3; }
    [zoom>17] { line-width: 10 + 3; }
  }
  [highway='service'],
  [highway='pedestrian'] {
    [zoom=16] { line-width: 1.6 + 2; }
    [zoom=17] { line-width: 2 + 2; }
    [zoom>17] { line-width: 3 + 2.5; }
  }
}

#bridges::case[zoom>=13][bridge=1] {
  line-cap:butt;
}

#motorways::fill[zoom>=6][zoom<=12],
#mainroads::fill[zoom>=10][zoom<=12],
#roads::fill[zoom>=13][tunnel!=1][bridge!=1],
#tunnels::fill[zoom>=13][tunnel=1],
#bridges::fill[zoom>=13][bridge=1] {
  // -- line style --
  line-cap:round;
  line-join:round;
  line-width:0;
  // -- colors --
  line-color:lighten(@road,20);
  [highway='motorway'],
  [highway='motorway_link'] {
    line-color:lighten(@motorway,10);
    [tunnel=1] { line-color:@motorway * 0.5 + rgb(127,127,127); }
  }
  [highway='trunk'],
  [highway='trunk_link'] {
    line-color:lighten(@trunk,10);
    [tunnel=1] { line-color:@trunk * 0.5 + rgb(127,127,127); }
  }
  [highway='primary'],
  [highway='primary_link'] {
    line-color:lighten(@primary,20);
    [tunnel=1] { line-color:@primary * 0.5 + rgb(127,127,127); }
  }
  [highway='secondary'],
  [highway='secondary_link'] {
    line-color:lighten(@secondary,20);
    [tunnel=1] { line-color:@secondary * 0.5 + rgb(127,127,127); }
  }
  // -- widths --
  [highway='motorway'],
  [highway='trunk'] {
    [zoom=12] { line-width: 1.2; }
    [zoom=13] { line-width: 2; }
    [zoom=14] { line-width: 4; }
    [zoom=15] { line-width: 6; }
    [zoom=16] { line-width: 9; }
    [zoom=17] { line-width: 13; }
    [zoom>17] { line-width: 15; }
  }
  [highway='primary'],
  [highway='secondary'] {
    [zoom=12] { line-width: 1; }
    [zoom=13] { line-width: 1.2; }
    [zoom=14] { line-width: 2; }
    [zoom=15] { line-width: 4; }
    [zoom=16] { line-width: 7; }
    [zoom=17] { line-width: 9; }
    [zoom>17] { line-width: 11; }
  }
  [highway='motorway_link'],
  [highway='trunk_link'],
  [highway='primary_link'],
  [highway='secondary_link'],
  [highway='tertiary'],
  [highway='tertiary_link'],
  [highway='unclassified'],
  [highway='residential'],
  [highway='living_street'] {
    [zoom=14] { line-width: 1.6; }
    [zoom=15] { line-width: 4; }
    [zoom=16] { line-width: 6; }
    [zoom=17] { line-width: 8; }
    [zoom>17] { line-width: 10; }
  }
  [highway='service'],
  [highway='pedestrian'] {
    [zoom=16] { line-width: 1.6; }
    [zoom=17] { line-width: 2; }
    [zoom>17] { line-width: 3; }
  }
}
*/
