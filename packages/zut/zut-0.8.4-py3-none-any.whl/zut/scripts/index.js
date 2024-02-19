/**
 * Utils for postinstall/prebuild scripts.
 */
import fs from 'fs'
import path from 'path'
import { execSync } from 'child_process'
import * as messages from './messages.js'

// Non-NodeJS requirements
import { globSync } from 'glob'


export { messages }

export function copy(pattern, target, {base} = {}) {
    if (base === undefined) {
        base = 'node_modules'
    }

    const files = globSync(pattern, {cwd: base})
    
    if (files.length == 0) {
        messages.error(`[copyStaticLib] ${pattern}: no file`)
        return
    }
    
    console.log(`[copyStaticLib] ${pattern}: ${files.length} file${files.length > 1 ? 's' : ''} ...`)
    
    for (const file of files) {
        const src = path.join(base, file)
        const dst = path.join(target, file)
        fs.mkdirSync(path.dirname(dst), {recursive: true})
        fs.copyFileSync(src, dst)
    }
}

const _cleanDirs = []

function inCleanDirs(file) {
    for (let cleanDir of _cleanDirs) {
        if (file.startsWith(`${cleanDir}${path.sep}`)) {
            return true
        }
    }
}

export function clean(pattern, {dryRun, ignore, noDefaultIgnore} = {}) {
    if (ignore === undefined) {
        ignore = []
    }

    if (!noDefaultIgnore) {
        for (const value of ['.venv/**', '.venv.*/**', 'node_modules/**', 'local/**']) {
            if (!pattern.includes(value) && !ignore.includes(value)) {
                ignore.push(value)
            }
        }
    }
    
    const files = globSync(pattern, {ignore: ignore})
    console.log(`[clean${dryRun ? ' dryrun' : ''}] ${pattern}: ${files.length} file${files.length > 1 ? 's' : ''} ...`)

    if (dryRun) {
        for (const file of files) {
            if (! inCleanDirs(file)) {
                messages.debug(`    ${file}`)
                if (fs.lstatSync(file).isDirectory()) {
                    _cleanDirs.push(file)
                }
            }
        }
    }
    else {
        for (const file of files) {
            messages.debug(`    ${file}`)
            fs.rmSync(file, {recursive: true, force: true})
        }
    }
}

export function run(cmd, {noException} = {}) {
    try {
        messages.debug(cmd) 
        execSync(cmd, {stdio: 'inherit'})
        return 0
    }
    catch (err) {
        const msg = `command exited with code ${err.status}`
        if (noException) {
            messages.error(msg)
            return err.status
        }
        else {
            throw new Error(msg)
        }
    }
}

export function getLastModifiedFile(dir) {
    const data_list = []

    for (const name of fs.readdirSync(dir)) {
        const file = path.join(dir, name)
        const stat = fs.statSync(file)
        if (stat.isDirectory()) {
            continue
        }
        data_list.push({file, mtime: stat.mtime.getTime()})
    }

    data_list.sort((fileA, fileB) => fileB.mtime - fileA.mtime)
    const data = data_list[0]
    return data !== undefined ? data.file : null
}
