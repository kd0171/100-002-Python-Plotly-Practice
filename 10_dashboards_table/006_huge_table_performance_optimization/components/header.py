from dash import html
import dash_bootstrap_components as dbc


header_product1 = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Product Dashboard", className="ms-2"),
        ]
    ),
    color="dark",
    dark=True,
)
