# How to use this example and fork from it

A published version of this example can be found here: https://cloud.viktor.ai/public/shapediver-karamba-integration-test

## Prerequisites

### Set up VIKTOR

Please follow VIKTOR's [Getting started](https://docs.viktor.ai/docs/getting-started/) guide and familiarize yourself with developing VIKTOR apps. 

The following steps assume that you installed the `viktor-cli` and have gained fundamental experience using VIKTOR. 

### Environment variables

This sample app makes use of environment variables to define which ShapeDiver model to communicate with. This allows you to avoid hardcoding critical information into your app. Please read the section on [environment variables](https://docs.viktor.ai/docs/create-apps/development-tools-and-tips/environment-variables) in VIKTOR's documentation. 

Set environment variables `SD_TICKET` and `SD_MODEL_VIEW_URL` according to the ShapeDiver model you want to use. 
Note that you need to enable [backend access](https://help.shapediver.com/doc/enable-backend-access) for your model. 

```
export SD_TICKET=718c311d77a31ceda3f463...                             # Use a backend ticket of your ShapeDiver model here
export SD_MODEL_VIEW_URL=https://sdr7euc1.eu-central-1.shapediver.com  # Use the model view url of your ShapeDiver model here
```

## Creating a VIKTOR parametrization for a ShapeDiver model

Once the environment variables are set, you can use the [`createParametrization.py`](createParametrization.py) script to help you create the parametrization for your VIKTOR app. 

An example:

```
$ python createParametrization.py 
param0 = NumberField('truss length [m]', name='ShapeDiverParams.06353841-58a1-41e8-966c-6ba817cce062', default=10, min=5, max=50, num_decimals=0, step=1, variant='slider')
param1 = NumberField('truss height [m]', name='ShapeDiverParams.6e1ea058-a76b-48aa-97df-666f93e474ba', default=1.2, min=0, max=5, num_decimals=1, step=0.1, variant='slider')
param2 = NumberField('truss bays', name='ShapeDiverParams.ff4000e1-51d2-4a62-b75a-e9297ca363d5', default=10, min=2, max=50, num_decimals=0, step=1, variant='slider')
param3Options = [OptionListElement('0', 'Selfweight'), OptionListElement('1', 'Point Load'), OptionListElement('2', 'Line Load'), OptionListElement('3', 'All')]
param3 = OptionField('LoadCase', name='ShapeDiverParams.6cc906cf-8cf3-4e3f-a185-affbf6e4fb55', options=param3Options, default=1)
param4 = NumberField('Point Load [kN]', name='ShapeDiverParams.5cd39465-987a-423e-b6d8-5e35a4e61f36', default=50, min=0, max=200, num_decimals=0, step=1.0, variant='slider')
param5 = NumberField('Position - Point Load', name='ShapeDiverParams.d43d900f-e6ec-4e00-9959-76f111124089', default=0.50, min=0, max=1, num_decimals=2, step=0.01, variant='slider')
param6 = NumberField('Line Load [kN/m]', name='ShapeDiverParams.f357c444-06e6-4380-a8d6-2ef175d74ce4', default=30, min=5, max=30, num_decimals=0, step=1.0, variant='slider')
param7 = BooleanField('Keep Compression Diagonals', name='ShapeDiverParams.c88a4330-8457-45a9-8020-15e241b360e5', default=False)
_param8Options = [OptionListElement('0', 'Cross Sec'), OptionListElement('1', 'Axial Stress'), OptionListElement('2', 'Utilisation'), OptionListElement('3', 'Displacement')]
param8 = OptionField('Render Settings', name='ShapeDiverParams.99459452-6f89-4c85-b0f3-3b258b1f2199', options=_param8Options, default='1')
param9 = NumberField('Deformation Scale', name='ShapeDiverParams.f582e03d-ec6f-4820-933e-a5ceefb9163e', default=100, min=0, max=100, num_decimals=0, step=1.0, variant='slider')
```

You can use this as a starting point for defining [input fields](https://docs.viktor.ai/docs/create-apps/user-input/) in [`app.py`](app.py).

## Local development

When running the app for local development in VIKTOR, make sure to pass on the environment variables to `viktor-cli` like this: 

```
viktor-cli start --env SD_TICKET=$SD_TICKET --env SD_MODEL_VIEW_URL=$SD_MODEL_VIEW_URL
```

## Publishing the app

Keep in mind to define the required [environment variables](https://docs.viktor.ai/docs/create-apps/development-tools-and-tips/environment-variables) for your published app.  

Have fun developing apps using ShapeDiver and VIKTOR! Should you have questions, check out the [ShapeDiver Help Center](https://help.shapediver.com/doc/) and our [Forum](https://forum.shapediver.com/). 
