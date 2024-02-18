# package:
#  dir: /path/to/SorS/
#  scripts:
#    - abbreviated-name: path/to/javascript/file # without extension, will be guessed based on scripts vs styles
projects = {
    'bootstrap': {
        'dir': 'dist',
        'scripts': {
            'bootstrap': 'js/bootstrap.min.js',
            'bootstrap-bundle': 'js/bootstrap.bundle.min.js'
        },
        'styles': {
            'bootstrap-min': 'css/bootstrap.min.css',
            'bootstrap-grid': 'css/bootstrap-grid.min.css',
            'bootstrap-reboot': 'css/bootstrap-reboot.min.css',
            'bootstrap-utilities': 'css/bootstrap-utilities.min.css'
        }
    },
    'htmx': {
        'dir': '.',
        'scripts': {
            'htmx': 'htmx.js'
        }
    },
    'jquery': {
        'dir': 'dist',
        'scripts': {
            'jquery': 'jquery.min.js'
        }
    },
    'react': {
        'dir': 'umd',
        'scripts': {
            'react': 'react.production.min.js'
        }
    },
    'tailwindcss': {
        'dir': 'dist',
        'styles': {
            'tailwind': 'tailwind.css'
        }
    }
}
