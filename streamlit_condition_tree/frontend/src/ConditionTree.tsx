import {ComponentProps, Streamlit, StreamlitComponentBase, withStreamlitConnection} from "streamlit-component-lib"
import React, {ReactNode} from "react"

import type {BuilderProps, Config, ImmutableTree, JsonGroup, JsonTree} from '@react-awesome-query-builder/antd';
import {AntdConfig, Builder, Query, Utils as QbUtils} from '@react-awesome-query-builder/antd';
import {ConfigProvider, theme as antdTheme} from 'antd';
import '@react-awesome-query-builder/antd/css/styles.css';
import './style.css'
import "@fontsource/source-sans-pro";
import {defaultConfig} from './config'


interface State {
    tree: ImmutableTree,
    config: Config
}

const defaultTree: JsonGroup = {
    type: "group",
    id: QbUtils.uuid()
};


const exportFunctions: Record<string, Function> = {
    queryString: QbUtils.queryString,
    mongodb: QbUtils.mongodbFormat,
    sql: QbUtils.sqlFormat,
    spel: QbUtils.spelFormat,
    elasticSearch: QbUtils.elasticSearchFormat,
    jsonLogic: QbUtils.jsonLogicFormat
}

const formatTree = (tree: any) => {
    // Recursively add uuid and rename 'children' key
    tree.id = QbUtils.uuid()
    if (tree.children) {
        tree.children1 = tree.children;
        delete tree.children;
        tree.children1.forEach(formatTree);
    }
};

const unformatTree = (tree: any) => {
    // Recursively remove uuid and rename 'children1' key
    delete tree.id;
    if (tree.children1) {
        tree.children = tree.children1;
        delete tree.children1;
        tree.children.forEach(unformatTree);
    }
};

class ConditionTree extends StreamlitComponentBase<State> {

    public constructor(props: ComponentProps) {
        super(props);

        console.log(AntdConfig)

        const config: Config = {
            ...defaultConfig,
            ...props.args['config']
        };

        // Load input tree
        let tree: ImmutableTree = QbUtils.loadTree(defaultTree)
        if (props.args['tree'] != null) {
            try {
                let input_tree = props.args['tree']
                formatTree(input_tree)
                tree = QbUtils.checkTree(QbUtils.loadTree(input_tree), config)
            } catch (error) {
                console.log(error);
            }
        }

        this.state = {config, tree}
        this.setStreamlitValue(tree)
    }

    public render = (): ReactNode => {
        const {theme} = this.props
        const tree = QbUtils.getTree(this.state.tree)
        const empty = !tree.children1 || !tree.children1.length

        return (
            <div>
                <ConfigProvider
                    theme={theme ? {
                        token: {
                            colorPrimary: theme['primaryColor'],
                            colorText: theme['textColor'],
                            fontFamily: theme['font'],
                            fontSize: 16,
                            controlHeight: 38,
                        },
                        algorithm: theme['base'] === 'dark' ?
                            antdTheme.darkAlgorithm : antdTheme.defaultAlgorithm
                    } : {}}
                >
                    <Query
                        {...this.state.config}
                        value={this.state.tree}
                        onChange={this.onChange}
                        renderBuilder={this.renderBuilder}
                    />
                    <p>{empty && this.props.args['placeholder']}</p>
                </ConfigProvider>
            </div>
        )
    }

    componentDidUpdate = () => {
        // Class to apply custom css on rule_groups with a single child
        document
            .querySelectorAll('.rule_group>.group--children:has(> :nth-child(1):last-child)')
            .forEach((x) => x.classList.add('single-child'))

        // Set frame height
        const height = Math.max(
            document.body.scrollHeight + 20,
            this.props.args['min_height']
        );
        Streamlit.setFrameHeight(height);
    }

    private onChange = (immutableTree: ImmutableTree) => {
        this.setState({tree: immutableTree})
        this.setStreamlitValue(immutableTree)
    }

    private setStreamlitValue = (tree: ImmutableTree) => {
        const exportFunc = exportFunctions[this.props.args['return_type']]
        const exportValue = exportFunc ? exportFunc(tree, this.state.config) : ''

        let output_tree: JsonTree = QbUtils.getTree(tree)
        unformatTree(output_tree)
        Streamlit.setComponentValue([output_tree, exportValue])
    }

    private renderBuilder = (props: BuilderProps) => (
        <div className="query-builder-container">
            <div className="query-builder qb-lite">
                <Builder {...props} />
            </div>
        </div>
    )
}

export default withStreamlitConnection(ConditionTree);
