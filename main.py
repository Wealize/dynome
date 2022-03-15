import os

import click
import heroku3


def get_premium_addons(addons):
    PREMIUM_ADDON_PLANS = ('standard', 'premium')

    premium_addons = []

    for addon in addons:
        if any(plan in addon.plan.name for plan in PREMIUM_ADDON_PLANS):
            premium_addons.append(addon.plan.name)

    return premium_addons


@click.command()
def dynome():
    '''Check which nodes are up on HEROKU'''
    c = heroku3.from_key(os.environ.get('HEROKU_API_KEY'))
    apps = c.apps(order_by='name')
    prod_apps = []
    staging_apps = []

    click.echo(click.style('Active Apps on Heroku', fg='red'))
    click.echo(click.style('---------------------', fg='red'))
    click.echo(click.style('Thinking, this could take a while...', fg='blue'))

    for app in apps:
        try:
            current_dyno = app.dynos()[0]

            if current_dyno.state == 'up':
                premium_addons = ','.join(get_premium_addons(app.addons()))
                line = f'{app.name} 🦖 {current_dyno.size} ➕ {premium_addons}'

                if 'staging' in app.name:
                    staging_apps.append(line)
                else:
                    prod_apps.append(line)

        except IndexError:
            # No Dynos on that app
            pass

    click.echo(click.style('STAGING', fg='red'))
    click.echo(click.style('-------', fg='red'))

    for item in staging_apps:
        click.echo(click.style(item, fg='cyan'))

    click.echo(click.style('PRODUCTION', fg='red'))
    click.echo(click.style('----------', fg='red'))

    for item in prod_apps:
        click.echo(click.style(item, fg='green'))


if __name__ == '__main__':
    dynome()
