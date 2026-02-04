#!/bin/bash
# Test script to verify node and npx are available

echo "Testing node and npx availability..."
echo ""

# Test node
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ node is installed: $NODE_VERSION"
else
    echo "✗ node is NOT installed"
    exit 1
fi

# Test npx
if command -v npx &> /dev/null; then
    NPX_VERSION=$(npx --version)
    echo "✓ npx is installed: $NPX_VERSION"
else
    echo "✗ npx is NOT installed"
    exit 1
fi

echo ""
echo "✓ All tools are available!"
exit 0

