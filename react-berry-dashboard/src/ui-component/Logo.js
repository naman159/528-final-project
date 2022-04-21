import React from 'react';

import { Typography } from '@material-ui/core';

// material-ui
import { useTheme } from '@material-ui/styles';

import logo from './../assets/images/logo.svg';

//-----------------------|| LOGO SVG ||-----------------------//
const ColoredLine = ({ color }) => (
    <hr
        style={{
            color: color,
            backgroundColor: color,
            height: 3
        }}
    />
);


const Logo = () => {
    const theme = useTheme();

    return (
        <div>
            <div className="d-flex flex-row mb-3">
              <img src={logo} alt="logo" width="30" />
              <Typography variant="body8">
                  Continuous Calibrex
              </Typography>
            </div>
            <ColoredLine color="grey" />
        </div>
    );
};

export default Logo;
