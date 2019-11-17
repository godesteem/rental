import {Typography} from "@material-ui/core";
import React, {useState} from "react";

export default function ProductDetail(props){
  const [product, setProduct] = useState(props.data || undefined)
  if(!product)
    return null
  return (<>
      <Typography>Price: {product.product.price} {product.product.currency}</Typography>
      <Typography>Components:</Typography>
      <ul>
        {product.warehouse_components && product.warehouse_components.map((elem, id) => (<li key={id}>{elem.component.name} x {elem.quantity}</li>))}
      </ul>
    </>
  )
}