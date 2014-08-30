module.exports = function (grunt) {

    grunt.file.defaultEncoding = 'utf8';

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        sass: {
            dist: {
                options: {
                    style: 'expanded'
                },
                files: [{
                    expand: true,
                    cwd: "<%= pkg.scss_src %>",
                    src: ['*.scss'],
                    dest: "<%= pkg.scss_src %>",
                    ext: '.css'
                }]
            }
        },

        watch: {
            files: ["<%= pkg.scss_src %>*.scss", "!<%= pkg.scss_src %>_brand.scss"],
            tasks: ['default']
        }

    });

    grunt.registerTask('initBrandScss', 'To clear brand css.', function () {
        grunt.file.write(grunt.config.get('pkg.scss_src') + "_brand.scss", "/*--This is file is used to override brand specific scss variables by grunt task--*/");
    });

    grunt.registerTask('upateBrandScss', 'To update with brand css values.', function () {
        var scss_src = grunt.config.get('pkg.scss_src');
        grunt.file.copy(scss_src + grunt.config.get('pkg.brand_file'), scss_src + "_brand.scss");
    });

    grunt.loadNpmTasks('grunt-preprocess');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['upateBrandScss', 'sass']);
};
