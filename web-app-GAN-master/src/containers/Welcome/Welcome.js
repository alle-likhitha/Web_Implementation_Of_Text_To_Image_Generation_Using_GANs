import React, {Component} from 'react';
import classes from "./Welcome.module.css";
// import birdimage from "../../assets/images/birdimage.jpg"
import Button from '../../ui/Button/Button';
import {GiHummingbird} from 'react-icons/gi'
import {FaEarlybirds} from 'react-icons/fa';
import {Link} from 'react-router-dom';

class Welcome extends Component{
    render(){
        return(
            <div className={classes.Welcome}>
                <div className={classes.Firstdiv}>
                <h1>Web Implementation of GAN's</h1>
                    <p><FaEarlybirds />  Welcome to our page  <FaEarlybirds /></p>
                    <p>What we do:</p>
                    {/* <p>blah blah balhlshd</p> */}
                    <p>We Generate bird images based on the input text given.</p>
                    <div className={classes.Seconddiv}>
                    {/* <Button iconname={{icon: GiHummingbird}}><Link to="/main"></Link></Button> */}
                    <Link to="/main" className={classes.NavItem}><Button iconname={{icon: GiHummingbird}}>Lets go</Button></Link>
                    </div>
                </div>
            </div>
        );
    }
}

export default Welcome;