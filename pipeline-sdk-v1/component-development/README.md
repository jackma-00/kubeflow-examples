# Organizing the component files

This section provides a recommended way to organize a component’s files. There is no requirement that you must organize the files in this way. However, using the standard organization makes it possible to reuse the same scripts for testing, image building, and component versioning.

components/component group/component name/

    src/*            # Component source code files
    tests/*          # Unit tests
    run_tests.sh     # Small script that runs the tests
    README.md        # Documentation. If multiple files are needed, move to docs/.

    Dockerfile       # Dockerfile to build the component container image
    build_image.sh   # Small script that runs docker build and docker push

    component.yaml   # Component definition in YAML format