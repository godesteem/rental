import {Typography} from "@material-ui/core";
import React, {useState} from "react";

export default function ComponentDetail(props){
  const component = props.data || undefined
  if(!component)
    return null
  return (<>
      <Typography>Storage Units:</Typography>
      <ul>
        {component.storage_units &&
        component.storage_units.map((elem, id) => {
          if(elem.storage_unit) {
            return (
              <li key={id}>{elem.storage_unit.name} x {elem.quantity}</li>
            )
          }
        })}
      </ul>
    </>
  )
}