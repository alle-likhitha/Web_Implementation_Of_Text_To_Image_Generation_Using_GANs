import React from 'react';
import classes from './Button.module.css';
// import { Link } from 'react-router-dom';
// import Aux from '../../hoc/Aux/Aux';


const Button = props =>{
    
    return(
        // <Link >
    //     <div className={classes.buttonSpace}>
    //        <props.iconname.icon className={classes.Icon}/>
    //         <button className={classes.Button} onClick={props.clicked}>{props.children}</button>
    //         {/* {props.children} */}
    //    </div>
        // </Link>
       
        <button className={classes.Button} onClick={props.clicked}>
        <div className={classes.buttonSpace}>
           <props.iconname.icon className={classes.Icon}/>
           {props.children}
           </div>
        </button>
        
            
);
}

export default Button;