import React, { Component } from "react";

import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';

const styles = theme => ({
    appBar: {
      top: 'auto',
      bottom: 0,
    },
});


class Footer extends Component {
  render() {

    const { classes } = this.props;


    return (
        <AppBar position="fixed" color="primary" className={classes.appBar}>
        SuperFooter
        </AppBar>
    );
  }
}

export default withStyles(styles)(Footer);
