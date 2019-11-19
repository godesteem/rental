import React from 'react';
import {Link} from "react-router-dom";
import OrderStats from "./OrderStats";
import {Grid} from "@material-ui/core";


export default function Overview(){
  return (
    <div>
      <Grid container spacing={3}>
        <Grid item md={6}>
          <Link to="/management/products">Products</Link><br/>
          <Link to="/management/components">Components</Link>
        </Grid>
        <Grid item md={6}>
          <OrderStats/>
        </Grid>
      </Grid>
    </div>
  )
}